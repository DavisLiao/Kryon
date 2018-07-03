`timescale 1ns / 1ps
`define W 48                     //Image Width  这两个定义需要根据输入测试图像的大小来修改. These two definitions need to be modified according to the size of the input test image.   
`define H 36                     //Image Height 忘了改结果就会不正确                        If you forgot, the result will be wrong
`define S `W * `H * 3            //图像数据的总字节数,由于是RGB数据,所以*3.                 Total bytes of the image
//This code comes from: https://github.com/becomequantum/kryon
//下面这篇文章介绍了FPGA图像处理基本技巧,The following article talks about FPGA Image Process,it's in Chinese, but Google translate is good enough:
//http://blog.sina.com.cn/s/blog_539ee1ae0102xtnz.html
//"tb1.txt"是文本格式的图像数据文件,里面存放的像素点的RGB值,你需要把你的图像文件转为文本格式做为仿真输入
//"tb1.txt" is the RGB value of the pixel data stored in the txt file. You need to convert your image file into text format for the simulation input.
module TestBench(

    );
    reg clk   ;          
    reg Vsync ;                  //垂直同步信号,也就是帧有效信号 Vertical Sync
    reg Hsync ;                  //水平同步信号,行有效           Horizontal Sync
    reg DataEn;                  //像素数据有效信号DE            Data Enable                    
    reg [7:0] R,G,B,GS,Dilation,Erosion,InBetween;                                                      
    reg [7:0] PicMem[0:`S-1];    //用来存储RGB图像数据 Used to store RGB image data                             
    integer h,l;                 //循环index
    integer PicFile1,PicFile2,PicFile3,PicFile4,PicFile5,PicFile6;
    integer i1 = 0,i2 = 0, n = 0;
    
    GrayOperator3x3 iGrayOperator3x3
    (
     .clk      (clk),         
     .DataEn   (DataEn),
     .PixelData(G),          //直接就把G值当灰度数据了
     .DataOutEn()    
    );
    
    BinaryOperator9x9 iBinaryOperator9x9
    (
     .clk      (clk   ),         
     .DataEn   (DataEn),
     .PixelData(G<128 ),      //比较黑的点变为1
     .DataOutEn()    
    );
    
    CCAL iCCAL
    (
     .clk       (clk   ),
     .Vsync     (Vsync ),
     .DataEn    (DataEn),
     .BinaryData(G<255 && R<255 && B<255),
     .OtherData (0),
     .DataOutEn (),
     .SumO      (),
     .XMaxO     (),
     .YMaxO     (),
     .XMinO     (),
     .YMinO     ()     
    );         
    
    always #5 clk = ~clk;
    
    initial begin
      clk   = 0;   
      Vsync = 0;
      Hsync = 0;
      DataEn= 0;
      R     = 0;
      G     = 0;
      B     = 0;
    	$readmemh("tb1.txt",PicMem);         //把tb1.txt中的图像数据读取到PicMem中来
    	PicFile6 = $fopen("CCAL.txt","w");   //This output is not an image data.
    	SimInput;
    	SimInput;
    	
    	$fclose(PicFile1);              
    	$fclose(PicFile2);
    	$fclose(PicFile3);              
    	$fclose(PicFile4);
    	$fclose(PicFile5);
    	$fclose(PicFile6);
    	$finish; 
    end
    
    task SimInput;                  //模拟VGA时序产生仿真图像输入. VGA Timing
    begin
    	#777; 
      @(posedge clk);
      #1;
	  	Vsync = 1;
	  	repeat(6) @(posedge clk);
	  	for(l=0;l<`H;l=l+1)           //Verilog里也可以写for循环,只不过是不可综合代码,只能在Test Bench里写写
	  	begin	  		
	  		Hsync = 1;
	  		repeat(5) @(posedge clk);             
	  		for(h=0;h<`W;h=h+1)  
	  		begin 
	  			#1;                       //仿真时使能和数据信号不要和时钟上升沿对齐,不同的仿真软件可能会对此有不同解读 
	  			DataEn = 1;
	  			R = PicMem[l*`W*3 + h*3]; G = PicMem[l*`W*3 + h*3 + 1]; B = PicMem[l*`W*3 + h*3 + 2];
	  			@(posedge clk);
	  		end  
	  		#1;                  
	  		DataEn = 0;
	  		R = 0; G = 0; B = 0;  
	  		repeat(7) @(posedge clk); 
	  		Hsync = 0;
	  		if(l<`H-1)
	  		  repeat(152) @(posedge clk);
	  		else
	  		  repeat(6) @(posedge clk);
	  	end 
	  	Vsync = 0;
      #111;
      
    end
    endtask
    
    always@(posedge Vsync)                     
      n <= n + 1;
    
    always@(negedge iCCAL.DataOutEn)              //输出连通域识别结果 Output connected component labeling results
      if(n == 1)
      begin
        $display("FPGA: Sum: %d XYmax: [%d,%d] XYmin: [%d,%d]\n",iCCAL.SumO,iCCAL.XMaxO,iCCAL.YMaxO,iCCAL.XMinO,iCCAL.YMinO); 
        $fwrite(PicFile6,"FPGA: Sum: %d XYmax: [%d,%d] XYmin: [%d,%d]\n",iCCAL.SumO,iCCAL.XMaxO,iCCAL.YMaxO,iCCAL.XMinO,iCCAL.YMinO);
      end
                                                               
    //把仿真结果再存为文本格式的图像数据                       
    initial                                                    
    begin                                                      
      PicFile1 = $fopen("GaussianBlur.txt","w");  //高斯平滑结果,文件会出现在ISE,Vivado等软件的仿真工作目录下 Gauss smoothing results, files will appear in ISE, Vivado and other software's simulation work directory.
      PicFile2 = $fopen("Sobel.txt","w");         //边缘检测结果 Edge detection results
      $fwrite(PicFile1,"%h %h\n",`W,`H);
      $fwrite(PicFile2,"%h %h\n",`W,`H);
      @(posedge iGrayOperator3x3.DataOutEn);  //3x3的算子结果会比原数据延时一行
      for(i1 = 0; i1 < `H; i1 = i1 + 1)
      begin
        @(posedge iGrayOperator3x3.DataOutEn)
        while(iGrayOperator3x3.DataOutEn == 1)
        begin
        	@(posedge clk); 
        	GS = iGrayOperator3x3.GaussianBlur;
        	$fwrite(PicFile1,"%H %H %H  ",GS, GS, GS); 
        	if(iGrayOperator3x3.Sobel == 0)
        	  $fwrite(PicFile2,"%H %H %H  ", GS, GS, GS);                //边缘检测的结果叠加在高斯平滑的结果上显示,边缘为蓝色       
        	else        
        	  $fwrite(PicFile2,"%H %H %H  ", 8'h0, 8'h0, 8'hff);  		   //这里要写8'h输出才是8位的,否则会是32位的.
        end     
          $fwrite(PicFile1,"\n");  
          $fwrite(PicFile2,"\n");
      end   
    end
    
    //保存9x9二值算子的计算结果.不同的initial块是并行的.
    initial 
    begin 
      PicFile3 = $fopen("Dilation.txt" ,"w");  
      PicFile4 = $fopen("Erosion.txt"  ,"w");    
      PicFile5 = $fopen("InBetween.txt","w");      
      $fwrite(PicFile3,"%h %h\n",`W,`H);
      $fwrite(PicFile4,"%h %h\n",`W,`H);
      $fwrite(PicFile5,"%h %h\n",`W,`H);
      repeat(4) @(posedge iBinaryOperator9x9.DataOutEn);               //9x9的算子结果会比原数据延时4行,因为中心点下面还有4行. The result of 9x9 is 4 rows later than the original data, because there are 4 rows below the center point.
      for(i2 = 0; i2 < `H; i2 = i2 + 1)                                //循环变量要换一个,不能和上面的相同
      begin
        @(posedge iBinaryOperator9x9.DataOutEn)
        while(iBinaryOperator9x9.DataOutEn == 1)
        begin
        	@(posedge clk); 
        	Dilation  = iBinaryOperator9x9.Dilation  ? 8'h0 : 8'hff; 
        	Erosion   = iBinaryOperator9x9.Erosion   ? 8'h0 : 8'hff;
        	InBetween = iBinaryOperator9x9.InBetween ? 8'h0 : 8'hff;
        	$fwrite(PicFile3,"%H %H %H  ",Dilation , Dilation , Dilation ); 
        	$fwrite(PicFile4,"%H %H %H  ",Erosion  , Erosion  , Erosion  ); 
        	$fwrite(PicFile5,"%H %H %H  ",InBetween, InBetween, InBetween);  		
        end     
          $fwrite(PicFile3,"\n");  
          $fwrite(PicFile4,"\n");
          $fwrite(PicFile5,"\n");
      end 
    end  
    
endmodule