using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using System.IO;
using System.Drawing.Imaging;
using System.Runtime.InteropServices;
using System.Timers;

namespace FPGA_UDP
{
    public partial class FPGA_UDP : Form
    {
        //arp -s 192.168.0.7 aa-bb-cc-dd-ee-ff 上位机要在cmd中输入这个命令手动绑定一下MAC和IP,这是FPGA的IP和MAC
        static Socket UDP_socket1;
        Thread ReceiveUdpDataThread;
        IPAddress myIP = IPAddress.Parse("192.168.0.91");       //上位机IP
        IPAddress remoteIP = IPAddress.Parse("192.168.0.7");    //FPGA IP
        bool 接收数据 = false;
        int PicRxbuffLength = 1024 * 512 * 3 + 54;
        byte[] PicRxbuff = new byte[1024 * 512 * 3 + 54 + 2 + 1024];//用于存储接收的图片, 前54字节用于存储BMP图片的文件头,后面的两个字节是因为FPGA程序多发了两个字节,这里多一点字节对后面的图片显示没影响
        int 异步接收字节计数 = 54;
        int 分包大小 = 1024; //FPGA拆分数据包的大小
        EndPoint remoteEP;
        bool 收完一帧 = true;

        public FPGA_UDP()
        {
            InitializeComponent();
            UDP_socket1 = new Socket(AddressFamily.InterNetwork, SocketType.Dgram, ProtocolType.Udp);
            UDP_socket1.ReceiveBufferSize = 1024 * 1024 * 1000 * 2; //Socket的缓冲区,满了没读出就不收了.最大就是这么大,大概2G字节
            UDP_socket1.Bind(new IPEndPoint(myIP, 57788)); //绑定端口号和IP,上位机接收数据端口号为57788
            Control.CheckForIllegalCrossThreadCalls = true;
            remoteEP = new IPEndPoint(remoteIP, 57788); //57788
            //BMP文件的前54字节文件头,这个文件头是1024*512的bmp文件文件头,用Ultra Editor打开一个1024*512的bmp文件就能看到
            PicRxbuff[0] = 0x42; PicRxbuff[1] = 0x4D; PicRxbuff[2] = 0x36; PicRxbuff[3] = 0x00; PicRxbuff[4] = 0x18; PicRxbuff[5] = 0x00; PicRxbuff[6] = 0x00; PicRxbuff[7] = 0x00; PicRxbuff[8] = 0x00; PicRxbuff[9] = 0x00; PicRxbuff[10] = 0x36; PicRxbuff[11] = 0x00; PicRxbuff[12] = 0x00; PicRxbuff[13] = 0x00; PicRxbuff[14] = 0x28; PicRxbuff[15] = 0x00;
            PicRxbuff[16] = 0x00; PicRxbuff[17] = 0x00; PicRxbuff[18] = 0x00; PicRxbuff[19] = 0x04; PicRxbuff[20] = 0x00; PicRxbuff[21] = 0x00; PicRxbuff[22] = 0x00; PicRxbuff[23] = 0x02; PicRxbuff[24] = 0x00; PicRxbuff[25] = 0x00; PicRxbuff[26] = 0x01; PicRxbuff[27] = 0x00; PicRxbuff[28] = 0x18; PicRxbuff[29] = 0x00; PicRxbuff[30] = 0x00; PicRxbuff[31] = 0x00;
            PicRxbuff[32] = 0x00; PicRxbuff[33] = 0x00; PicRxbuff[34] = 0x00; PicRxbuff[35] = 0x00; PicRxbuff[36] = 0x00; PicRxbuff[37] = 0x00; PicRxbuff[38] = 0xc4; PicRxbuff[39] = 0x0e; PicRxbuff[40] = 0x00; PicRxbuff[41] = 0x00; PicRxbuff[42] = 0xc4; PicRxbuff[43] = 0x0e; PicRxbuff[44] = 0x00; PicRxbuff[45] = 0x00; PicRxbuff[46] = 0x00; PicRxbuff[47] = 0x00;
            PicRxbuff[48] = 0x00; PicRxbuff[49] = 0x00; PicRxbuff[50] = 0x00; PicRxbuff[51] = 0x00; PicRxbuff[52] = 0x00; PicRxbuff[53] = 0x00;
        }

        private void StartRx_Click(object sender, EventArgs e)
        {
            if (StartRx.Text == "全速接收")
            {
                StartRx.Text = "停止接收";
                接收数据 = true;
                labelCNT1.Text = "0";
                ReceiveUdpDataThread = new Thread(new ThreadStart(ReceiveUdpData));
                ReceiveUdpDataThread.IsBackground = true;
                ReceiveUdpDataThread.Start();
            }
            else
            {
                StartRx.Text = "全速接收";
                接收数据 = false;
            }
        }

        private void ReceiveUdpData()
        {
            int 收包计数 = 54; //数据是收到用来存储图片的buffer中,从第54开始,前面已经存了文件头.
            bool 图片发送请求已发送 = false;
            byte[] tempbuff = new byte[1024]; //临时buffer,用来收空UDP Buffer中的数据
            while (接收数据) //不限帧率连续接受图像.收完一帧就立即请求发下一帧
            {     
                
                if(图片发送请求已发送 == false)
                {

                    while (UDP_socket1.Available > 0)    //先把UDP Buffer中可能残留的数据读空
                    {
                        UDP_socket1.ReceiveFrom(tempbuff, ref remoteEP);
                    }
                    NoteFPGA();                          //向FPGA发送7字节发送图片请求
                    图片发送请求已发送 = true;           //限制每帧只发一次
                }

                if (UDP_socket1.Available > 1) //接收数据
                {
                    收包计数 += UDP_socket1.ReceiveFrom(PicRxbuff, 收包计数, UDP_socket1.Available, SocketFlags.None, ref remoteEP);
                }
                if(收包计数 >= PicRxbuffLength ) //收满了一帧图像的字节数,这里用>=是因为FPGA在最后还多发了两个字节,所以在前面也要先读空.
                {
                    try
                    {
                        Image img = Image.FromStream(new MemoryStream(PicRxbuff));//把字节数组转成内存流显示.
                        ShowBMP(pictureBox1, img);
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show(ex.Message);
                    }
                    收包计数 = 54;                //一帧收完显示完后复位计数
                    图片发送请求已发送 = false;   //开启发送请求.
                   
                }
                  
            }

        }

        delegate void LabelDelegate(Label label, string text);
        private void LabelText(Label label, string text)
        {
            if (label.InvokeRequired)
            {
                LabelDelegate d = LabelText;
                label.Invoke(d, new object[] { label, text });
            }
            else
            {
                label.Text = text;

            }
        }

        delegate void AppendTextDelegate(RichTextBox richtextbox, string text);
        private void AppendText(RichTextBox richtextbox, string text)
        {
            if (richtextbox.InvokeRequired)
            {
                AppendTextDelegate d = AppendText;
                richtextbox.Invoke(d, new object[] { richtextbox, text });
            }
            else
            {
                richtextbox.AppendText(text + "\n");
            }
        }
        delegate void ShowBMPDelegate(PictureBox picbox, Image img);
        private void ShowBMP(PictureBox picbox, Image img)
        {
            if (picbox.InvokeRequired)
            {
                ShowBMPDelegate d = ShowBMP;
                picbox.Invoke(d, new object[] { picbox, img });
            }
            else
            {
                picbox.Image = img;
            }
        }

        private void SendPkt_Click(object sender, EventArgs e)
        {
            byte[] tempbuff = new byte[7];
            EndPoint remoteEP = new IPEndPoint(remoteIP, 57766);
            UDP_socket1.SendTo(tempbuff, remoteEP);           
        }

        private void Clear_Click(object sender, EventArgs e)
        {
            richTextBox1.Clear();
        }

        private void FixedFrameRate_Click(object sender, EventArgs e)
        {
            if (FixedFrameRate.Text == "固定帧率接收") //1024*512的bmp图片全速接收时能到64帧,数据速率大概是100.6M字节/秒,基本达到千兆网实际传输速度上限
            {                                          //实际应用中可能用不着这么高的帧率,所以可以用个定时器定时触发,限定一下帧率.
                FixedFrameRate.Text = "停止接收";      //这里timer设置的是40ms,实测帧率为21帧左右.设置30ms帧率能到32
                FrameRateTimer.Start();
                
            }
            else
            {
                FixedFrameRate.Text = "固定帧率接收";
                FrameRateTimer.Stop();
            }
        }

        private void AsyncReceive(IAsyncResult ar) //异步法貌似略慢
        {
            var UDPsocket = ar.AsyncState as Socket;
            异步接收字节计数 += UDPsocket.EndReceive(ar);
            if (异步接收字节计数 < PicRxbuffLength)
            {
                 UDPsocket.BeginReceive(PicRxbuff, 异步接收字节计数, 分包大小, SocketFlags.None, new AsyncCallback(AsyncReceive), UDPsocket);                          
            }
            else
            {
                MemoryStream ms = new MemoryStream(PicRxbuff);//把字节数组转成内存流显示.
                try
                {
                    Image img = Image.FromStream(ms);
                    ShowBMP(pictureBox1, img);
                }
                catch (Exception ex)
                {
                    MessageBox.Show(ex.Message);
                }
                收完一帧 = true;
            }     
           
            
        }

        private void NoteFPGA()
        {
            EndPoint remoteEPrx = new IPEndPoint(remoteIP, 57766);//57766 上位机在接收每帧数据之前会用57766这个端口发给FPGA一个7字节的数据包,示意FPGA网上发一帧的数据
            byte[] NoteFPGAtoStartbuff = new byte[7];
            UDP_socket1.SendTo(NoteFPGAtoStartbuff, remoteEPrx);  //向FPGA发送7字节发送图片请求
        }

        private void FrameRateTimer_Tick(object sender, EventArgs e)
        {
            if (收完一帧 == true)
            {
                收完一帧 = false;                 //防止上一帧没收完又开始下一帧
                异步接收字节计数 = 54;
                byte[] tempbuff = new byte[1024]; //临时buffer,用来收空UDP Buffer中的数据
                while (UDP_socket1.Available > 0)    //先把UDP Buffer中可能残留的数据读空
                {
                    UDP_socket1.ReceiveFrom(tempbuff, ref remoteEP);
                }
                UDP_socket1.BeginReceive(PicRxbuff, 异步接收字节计数, 分包大小, SocketFlags.None, new AsyncCallback(AsyncReceive), UDP_socket1);//用异步法接收,用同步法也可以,都一样,异步法似乎还慢一点
                NoteFPGA();
            }
            
        }
    }
}
