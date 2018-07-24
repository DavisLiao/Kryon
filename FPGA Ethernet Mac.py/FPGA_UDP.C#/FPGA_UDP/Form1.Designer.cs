namespace FPGA_UDP
{
    partial class FPGA_UDP
    {
        /// <summary>
        /// 必需的设计器变量。
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// 清理所有正在使用的资源。
        /// </summary>
        /// <param name="disposing">如果应释放托管资源，为 true；否则为 false。</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows 窗体设计器生成的代码

        /// <summary>
        /// 设计器支持所需的方法 - 不要修改
        /// 使用代码编辑器修改此方法的内容。
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            this.pictureBox1 = new System.Windows.Forms.PictureBox();
            this.labelCNT1 = new System.Windows.Forms.Label();
            this.StartRx = new System.Windows.Forms.Button();
            this.SendPkt = new System.Windows.Forms.Button();
            this.richTextBox1 = new System.Windows.Forms.RichTextBox();
            this.Clear = new System.Windows.Forms.Button();
            this.FixedFrameRate = new System.Windows.Forms.Button();
            this.FrameRateTimer = new System.Windows.Forms.Timer(this.components);
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).BeginInit();
            this.SuspendLayout();
            // 
            // pictureBox1
            // 
            this.pictureBox1.Location = new System.Drawing.Point(2, 2);
            this.pictureBox1.Name = "pictureBox1";
            this.pictureBox1.Size = new System.Drawing.Size(1024, 512);
            this.pictureBox1.TabIndex = 0;
            this.pictureBox1.TabStop = false;
            // 
            // labelCNT1
            // 
            this.labelCNT1.AutoSize = true;
            this.labelCNT1.Location = new System.Drawing.Point(1032, 9);
            this.labelCNT1.Name = "labelCNT1";
            this.labelCNT1.Size = new System.Drawing.Size(11, 12);
            this.labelCNT1.TabIndex = 1;
            this.labelCNT1.Text = "0";
            // 
            // StartRx
            // 
            this.StartRx.Location = new System.Drawing.Point(1034, 24);
            this.StartRx.Name = "StartRx";
            this.StartRx.Size = new System.Drawing.Size(75, 23);
            this.StartRx.TabIndex = 2;
            this.StartRx.Text = "全速接收";
            this.StartRx.UseVisualStyleBackColor = true;
            this.StartRx.Click += new System.EventHandler(this.StartRx_Click);
            // 
            // SendPkt
            // 
            this.SendPkt.Location = new System.Drawing.Point(1034, 53);
            this.SendPkt.Name = "SendPkt";
            this.SendPkt.Size = new System.Drawing.Size(75, 23);
            this.SendPkt.TabIndex = 3;
            this.SendPkt.Text = "发个包";
            this.SendPkt.UseVisualStyleBackColor = true;
            this.SendPkt.Click += new System.EventHandler(this.SendPkt_Click);
            // 
            // richTextBox1
            // 
            this.richTextBox1.Location = new System.Drawing.Point(1034, 82);
            this.richTextBox1.Name = "richTextBox1";
            this.richTextBox1.Size = new System.Drawing.Size(156, 565);
            this.richTextBox1.TabIndex = 4;
            this.richTextBox1.Text = "";
            // 
            // Clear
            // 
            this.Clear.Location = new System.Drawing.Point(1116, 53);
            this.Clear.Name = "Clear";
            this.Clear.Size = new System.Drawing.Size(75, 23);
            this.Clear.TabIndex = 5;
            this.Clear.Text = "清空";
            this.Clear.UseVisualStyleBackColor = true;
            this.Clear.Click += new System.EventHandler(this.Clear_Click);
            // 
            // FixedFrameRate
            // 
            this.FixedFrameRate.Location = new System.Drawing.Point(1116, 24);
            this.FixedFrameRate.Name = "FixedFrameRate";
            this.FixedFrameRate.Size = new System.Drawing.Size(92, 23);
            this.FixedFrameRate.TabIndex = 6;
            this.FixedFrameRate.Text = "固定帧率接收";
            this.FixedFrameRate.UseVisualStyleBackColor = true;
            this.FixedFrameRate.Click += new System.EventHandler(this.FixedFrameRate_Click);
            // 
            // FrameRateTimer
            // 
            this.FrameRateTimer.Interval = 10;
            this.FrameRateTimer.Tick += new System.EventHandler(this.FrameRateTimer_Tick);
            // 
            // FPGA_UDP
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 12F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1210, 659);
            this.Controls.Add(this.FixedFrameRate);
            this.Controls.Add(this.Clear);
            this.Controls.Add(this.richTextBox1);
            this.Controls.Add(this.SendPkt);
            this.Controls.Add(this.StartRx);
            this.Controls.Add(this.labelCNT1);
            this.Controls.Add(this.pictureBox1);
            this.Name = "FPGA_UDP";
            this.Text = "FPGA_UDP";
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.PictureBox pictureBox1;
        private System.Windows.Forms.Label labelCNT1;
        private System.Windows.Forms.Button StartRx;
        private System.Windows.Forms.Button SendPkt;
        private System.Windows.Forms.RichTextBox richTextBox1;
        private System.Windows.Forms.Button Clear;
        private System.Windows.Forms.Button FixedFrameRate;
        private System.Windows.Forms.Timer FrameRateTimer;
    }
}

