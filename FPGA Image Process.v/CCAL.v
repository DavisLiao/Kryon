`timescale 1ns / 1ps
//This code comes from: https://github.com/becomequantum/kryon
//下面这篇文章介绍了该算法的思路,The following article introduces the idea of the algorithm,it's in Chinese, but Google translate is good enough:
//http://blog.sina.com.cn/s/blog_539ee1ae0102xtod.html
//本模块是连通域识别并行流水线法的实现, 你可能需要参考该算法python版代码CCAL.py来理解本.v代码
//This module implements Parallel Pipeline Method of Connected Component Analysis-Labeling, To better understand this .v code, you may refer to the python version: CCAL.py
//本代码只进行过少量仿真测试,不能保证完全没有问题. This code has only conducted a small number of simulation tests, which can not guarantee that there is no bug.
//已知问题有:类似bug.bmp中下面两个结构的连通域在识别时会出现漏统计的问题,具体请见上述文章.
//The known problems are: like the structures of the below two shapes in bug.bmp, there will be leak statistics when labeling. Read above article for more details
`define ADDR_WIDTH        11
`define D                 3
module CCAL(
  input                       clk       ,   
  input                       Vsync     ,  
  input                       DataEn    ,
  input                       BinaryData,   //二值图像数据,Binary Image data
  input  [6:0]                OtherData ,   //可以顺便用来统计一些其它东西,比如该形状中有多少个某种颜色的点. It can be used to count some other things, such as the number of some colored dots in this shape.
  output reg                  DataOutEn ,
  output reg [31:0]           SumO      ,
  output reg [15:0]           XMaxO     ,
  output reg [15:0]           YMaxO     ,
  output reg [15:0]           XMinO     ,
  output reg [15:0]           YMinO     
  
  );
  
  reg [9 :0] LabelCount = 1;
  reg [15:0] FrogCount = 0, Y = 0;
  reg [9 :0] Left_RealLabel, UpLeft_RealLabel, Up_RealLabel, Old_Label,Old_Label1,Old_Label2,Left_RealLabel_reg,UpRight_Label,Up_Label,UpLeft_Label;
  reg [31:0] Left_Sum, UpLeft_Sum, Up_Sum,Left_Sum_reg;
  reg [15:0] Left_XMax, UpLeft_XMax, Up_XMax, Left_YMax, UpLeft_YMax, Up_YMax, Left_XMax_reg,Left_XMin_reg,Left_XLMax_reg,
             Left_XMin, UpLeft_XMin, Up_XMin, Left_YMin, UpLeft_YMin, Up_YMin, Left_YMax_reg,Left_YMin_reg,
             Left_XLMax, UpLeft_XLMax, Up_XLMax;
  reg        Vsync1,Left_Dot,Middle_Dot,RightDot,Diff_Label;
  reg [`D:0] DataEnReg;
  reg [ 1:0] DotReg;
  wire [179:0] SIdouta,SIdoutaTemp; 
  wire [31:0] UpRight_Sum; 
  wire [15:0] UpRight_XMax,UpRight_YMax,UpRight_XMin,UpRight_YMin,UpRight_XLMax;    
  wire [9 :0] UpRight_RealLabel;  
  
  wire [15:0] X = FrogCount - 3;
  wire [2 :0] NumOfLabeled = (Left_RealLabel > 0) + (UpLeft_RealLabel > 0) + (Up_RealLabel > 0) + (UpRight_RealLabel > 0);
  wire [31:0] Left_UpRight_Sum  = Left_Sum + UpRight_Sum + 1;
  wire [15:0] Left_UpRight_XMax = MAX(Left_XMax,UpRight_XMax);
  wire [15:0] Left_UpRight_XMin = MIN(Left_XMin,UpRight_XMin);
  wire [15:0] Left_UpRight_YMin = MIN(Left_YMin,UpRight_YMin);   
  wire [31:0] UpLeft_UpRight_Sum  = UpLeft_Sum + UpRight_Sum + 1; 
  wire [15:0] UpLeft_UpRight_XMax = MAX(UpLeft_XMax,UpRight_XMax);
  wire [15:0] UpLeft_UpRight_XMin = MIN(UpLeft_XMin,UpRight_XMin);
  wire [15:0] UpLeft_UpRight_YMin = MIN(UpLeft_YMin,UpRight_YMin);  
 
  
  assign {UpRight_RealLabel,UpRight_XLMax,UpRight_YMin,UpRight_XMin,UpRight_YMax,UpRight_XMax,UpRight_Sum} 
        = ( SIwebCombineDatareg && (SIdouta[121:112] > 0) ) ||  ( SIwebNewDatareg && (SIdouta[121:112] == SIdinbWebreg[121:112]) ) ? SIdinbWebreg[121:0] :  SIdouta[121:0] ;
         
  wire L_UpR_Diff = Middle_Dot &&  ((Left_RealLabel != UpRight_RealLabel) && Left_RealLabel > 0 );
  wire Two_Diff   = Middle_Dot &&  (( L_UpR_Diff || ( (UpLeft_RealLabel != UpRight_RealLabel) && UpLeft_RealLabel >0)) && UpRight_RealLabel > 0 );
  wire SIwebCombineData  = Two_Diff;
  wire[179:0] SIdinbWeb2 = L_UpR_Diff ? {0,Left_RealLabel  ,X,  Left_UpRight_YMin,  Left_UpRight_XMin,Y,  Left_UpRight_XMax,Left_UpRight_Sum} 
                                      : {0,UpLeft_RealLabel,X,UpLeft_UpRight_YMin,UpLeft_UpRight_XMin,Y,UpLeft_UpRight_XMax,UpLeft_UpRight_Sum};   
  reg [179:0] SIdinbWebreg;    
  reg         SIwebCombineDatareg,SIwebNewDatareg;                               
  wire SIwebNewData     = Left_Dot && !Middle_Dot;
  wire SIwebOld_Label1  = !SIwebCombineData && Middle_Dot && !RightDot;

                                      
  always@(posedge clk)  
  begin
  	SIwebCombineDatareg <= SIwebCombineData; SIwebNewDatareg <= SIwebNewData;	DataOutEn <= 0;   	   
  	Up_Sum       <= UpRight_Sum      ; UpLeft_Sum       <= Up_Sum      ; Left_Sum <= 0;
    Up_XMax      <= UpRight_XMax     ; UpLeft_XMax      <= Up_XMax     ; Left_XMax <= 0;
    Up_YMax      <= UpRight_YMax     ; UpLeft_YMax      <= Up_YMax     ; Left_YMax <= 0; 
    Up_XMin      <= UpRight_XMin     ; UpLeft_XMin      <= Up_XMin     ; Left_XMin <= 0;
    Up_YMin      <= UpRight_YMin     ; UpLeft_YMin      <= Up_YMin     ; Left_YMin <= 0; 
    Up_XLMax     <= UpRight_XLMax    ; UpLeft_XLMax     <= Up_XLMax    ; Left_XLMax <= 0;
    Up_RealLabel <= UpRight_RealLabel; UpLeft_RealLabel <= Up_RealLabel; Left_RealLabel <= 0;
    
    
    if(Middle_Dot)            //black dot   
      if(NumOfLabeled == 0)     //new unlabeled black dot
      begin
      	Left_RealLabel <= LabelCount; Left_Sum <= 1; Left_XMax <= X; Left_YMax <= Y; Left_XMin <= X; Left_YMin <= Y; Left_XLMax <= X;
      	if(LabelCount == 10'b11_1111_1111)   //不能等于0, cannot be 0.
      	  LabelCount <= 1;
      	else
      	  LabelCount <= LabelCount + 1; 	  
      end
      
      else if(Two_Diff)
      begin                     //Two different labeled dot around, needs merge data, label
      	if(L_UpR_Diff)
      	begin
      		Left_Sum  <= Left_UpRight_Sum ; Left_XMax <= Left_UpRight_XMax;  Left_YMax  <= Y;    Left_RealLabel <= Left_RealLabel;
      		Left_XMin <= Left_UpRight_XMin; Left_YMin <= Left_UpRight_YMin;  Left_XLMax <= X;
      		
      		//下面的赋值是为了流水线寄存器的数据和当前数据保持一致.The assignment below is to keep the data of the pipeline register consistent with the current data.
      		Up_Sum    <= Left_UpRight_Sum ; Up_XMax   <= Left_UpRight_XMax;  Up_YMax  <= Y;      Up_RealLabel <= Left_RealLabel;
      		Up_XMin   <= Left_UpRight_XMin; Up_YMin   <= Left_UpRight_YMin;  Up_XLMax <= X;  		
      	end
      	else
      	begin
      		Left_Sum  <= UpLeft_UpRight_Sum;  Left_XMax <= UpLeft_UpRight_XMax; Left_YMax  <= Y;  Left_RealLabel <= UpLeft_RealLabel;
      		Left_XMin <= UpLeft_UpRight_XMin; Left_YMin <= UpLeft_UpRight_YMin; Left_XLMax <= X;
      		Up_Sum    <= UpLeft_UpRight_Sum;  Up_XMax   <= UpLeft_UpRight_XMax; Up_YMax    <= Y;  Up_RealLabel <= UpLeft_RealLabel;
      		Up_XMin   <= UpLeft_UpRight_XMin; Up_YMin   <= UpLeft_UpRight_YMin; Up_XLMax   <= X;      		
      	end     	
      end      
      else                      //Only One Label value around
      begin
      	{Left_RealLabel,Left_XLMax,Left_YMin,Left_XMin,Left_YMax,Left_XMax,Left_Sum} <= 
      	{Left_RealLabel_reg,Left_XLMax_reg,Left_YMin_reg,Left_XMin_reg,Left_YMax_reg,Left_XMax_reg,Left_Sum_reg};     	
      end                     
    else                      //white dot
    begin
    	if(!Left_Dot && !RightDot && Up_RealLabel > 0 && UpRight_RealLabel == 0)
    	  if(Up_XLMax == X && Up_YMax == Y - 1)
    	  begin
    	    DataOutEn <= 1;                         
    	    SumO <= Up_Sum; XMaxO <= Up_XMax; YMaxO <= Up_YMax; XMinO <= Up_XMin; YMinO <= Up_YMin;
    	  end
    end   
    
    //保持数据一致 Keep the data consistent
    if(SIwebNewData && UpRight_RealLabel == Left_RealLabel)
    begin
    	{Up_RealLabel,Up_XLMax,Up_YMin,Up_XMin,Up_YMax,Up_XMax,Up_Sum} <= {Left_RealLabel,Left_XLMax,Left_YMin,Left_XMin,Left_YMax,Left_XMax,Left_Sum};
    end    
    if(SIwebNewData && Up_RealLabel == Left_RealLabel)
    begin
    	{UpLeft_RealLabel,UpLeft_XLMax,UpLeft_YMin,UpLeft_XMin,UpLeft_YMax,UpLeft_XMax,UpLeft_Sum} <= {Left_RealLabel,Left_XLMax,Left_YMin,Left_XMin,Left_YMax,Left_XMax,Left_Sum};
    end 
    
    //把数据写回已被合并掉的标号中,Write the data back into the merged label
    if(SIwebCombineData)
    begin
      Old_Label1 <= UpRight_RealLabel; 
      Old_Label2 <= Old_Label1;
    end
    else if(Diff_Label)
    begin
    	Old_Label1 <= Old_Label;
    end
    else
    begin
      if(SIwebNewDatareg)
        Old_Label2 <= 0;
      if(SIwebOld_Label1 || SIwebNewDatareg)
        Old_Label1 <= 0;
    end
    
    if(SIwebCombineData)
      SIdinbWebreg <= SIdinbWeb2;
    else
      SIdinbWebreg <= {Left_RealLabel,Left_XLMax,Left_YMin,Left_XMin,Left_YMax,Left_XMax,Left_Sum};       
                                           
  end  
  
  always@(*)                    //Only One Label value around  
    if(Left_RealLabel > 0)                                                                                                     
    begin                                                                                                                      
    	Left_Sum_reg  = Left_Sum + 1;      Left_XMax_reg = MAX(X,Left_XMax); Left_YMax_reg  = Y; Left_RealLabel_reg = Left_RealLabel;        
      Left_XMin_reg = MIN(X,Left_XMin);  Left_YMin_reg = MIN(Y,Left_YMin); Left_XLMax_reg = X;      
      Diff_Label = 0;
      Old_Label  = 0;                    
    end                                                                                                                        
    else if(UpRight_RealLabel > 0)                                                                                             
    begin                                                                                                                      
    	Left_Sum_reg  = UpRight_Sum + 1;     Left_XMax_reg = MAX(X,UpRight_XMax); Left_YMax_reg  = Y; Left_RealLabel_reg = UpRight_RealLabel;
    	Left_XMin_reg = MIN(X,UpRight_XMin); Left_YMin_reg = MIN(Y,UpRight_YMin); Left_XLMax_reg = X;  
    	if(UpRight_RealLabel != UpRight_Label) 
    	begin
    		Diff_Label = 1;
    		Old_Label  = UpRight_Label;
    	end                                  
    end                                                                                                                        
    else if(Up_RealLabel > 0)                                                                                                  
    begin                                                                                                                      
    	Left_Sum_reg  = Up_Sum + 1;     Left_XMax_reg = MAX(X,Up_XMax); Left_YMax_reg  = Y; Left_RealLabel_reg = Up_RealLabel;               
    	Left_XMin_reg = MIN(X,Up_XMin); Left_YMin_reg = MIN(Y,Up_YMin); Left_XLMax_reg = X; 
    	if(Up_RealLabel != Up_Label) 
    	begin
    		Diff_Label = 1;
    		Old_Label  = Up_Label;
    	end                                                  
    end       	                                                                                                               
    else if(UpLeft_RealLabel > 0)                                                                                              
    begin                                                                                                                      
    	Left_Sum_reg  = UpLeft_Sum + 1;     Left_XMax_reg = MAX(X,UpLeft_XMax); Left_YMax_reg  = Y; Left_RealLabel_reg = UpLeft_RealLabel;   
    	Left_XMin_reg = MIN(X,UpLeft_XMin); Left_YMin_reg = MIN(Y,UpLeft_YMin); Left_XLMax_reg = X;  
    	if(UpLeft_RealLabel != Up_RealLabel) 
    	begin
    		Diff_Label = 1;
    		Old_Label  = Up_RealLabel;
    	end                                         
    end      	      	                                                                                                                                                 
                                                 
  wire LineEnable = DataEn || DataEnReg[`D];
  
  always@(posedge clk)
  begin
    if(LineEnable)
      FrogCount <= FrogCount + 1;                                 //计数用以产生读写Ram的地址. Generate Ram reading address
    else            
      FrogCount <= 0;   
        
    UpLeft_Label <= Up_Label; Up_Label <= UpRight_Label; UpRight_Label <= SIaddra;
    Left_Dot         <= Middle_Dot  ; Middle_Dot <= RightDot; RightDot <= DotReg[0]; 
    Vsync1           <= Vsync;
    DataEnReg[0]     <= DataEn;
    DataEnReg[`D:1]  <= DataEnReg[`D - 1:0];
    DotReg[1]        <= DotReg[0];
    if(DataEn)
      DotReg[0]      <= BinaryData;
    else
      DotReg[0]      <= 0;
    if(FrameStart)
      Y <= 0;
    else if(LineEnd)
      Y <= Y + 1;
  end
  
  wire FrameStart = Vsync && !Vsync1;  
  wire LineEnd = DataEnReg[`D] && !DataEnReg[`D - 1];
  wire LineStart = DataEn && !DataEnReg[0];
  
  function [15:0] MAX;
    input [15:0] a,b;
    MAX = a > b ? a : b;
  endfunction
  
  function [15:0] MIN;
    input [15:0] a,b;
    MIN = a < b ? a : b;
  endfunction
  
  wire [`ADDR_WIDTH - 1 : 0] LAaddra = FrogCount;
  wire [17              : 0] LAdouta;
  wire [179             : 0] SIdinb  = SIwebNewData ? {0,Left_RealLabel,Left_XLMax,Left_YMin,Left_XMin,Left_YMax,Left_XMax,Left_Sum} :
                                                 (SIwebNewDatareg ? SIdinbWebreg :
                                                 (SIwebOld_Label1 ? {0,Left_RealLabel_reg,Left_XLMax_reg,Left_YMin_reg,Left_XMin_reg,Left_YMax_reg,Left_XMax_reg,Left_Sum_reg} : SIdinbWeb2) );
  wire                       SIweb   = SIwebNewData || SIwebCombineData || (SIwebNewDatareg && Old_Label2!= 0) || ( !SIwebCombineData && (SIwebOld_Label1 && Old_Label1!= 0) ); 
  wire [9               : 0] SIaddrb = SIwebNewData ? SIdinb[121:112] :
                                                 (SIwebNewDatareg ? Old_Label2 : 
                                                  (SIwebOld_Label1 ? Old_Label1 : UpRight_RealLabel) );
  wire [`ADDR_WIDTH - 1 : 0] LAaddrb = FrogCount - `D - 1;
  wire [17              : 0] LAdinb  = {/*OtherData*/0,Left_RealLabel,Left_Dot};    
  wire                       LAweb   = DataEnReg[`D];  
  
  wire [9               : 0] SIaddra = LAdouta[10:1] ;
  wire                       SIwea   =  0;
  wire [179             : 0] SIdina  =  0;
  
  
  //生成这几个Ram时需让其初值为0, 
  //Set the init value of these Rams to 0 when you generate it
  BlockRam180x1024 iShapeInfoList (
   .clka (clk        ),  // input wire clka
   .wea  (SIwea      ),  // input wire [0 : 0] wea
   .addra(SIaddra    ),  // input wire [9 : 0] addra
   .dina (SIdina     ),  // input wire [179 : 0] dina
   .douta(SIdouta    ),  // output wire [179 : 0] douta
   .clkb (clk        ),  // input wire clkb
   .web  (SIweb      ),  // input wire [0 : 0] web
   .addrb(SIaddrb    ),  // input wire [9 : 0] addrb
   .dinb (SIdinb     ),  // input wire [179 : 0] dinb
   .doutb(           )   // output wire [179 : 0] doutb
  );
  
  BlockRam18x2048 iLabelArray (
   .clka (clk    ),  // input  wire          clka
   .wea  (0      ),  // input  wire [0  : 0] wea     
   .addra(LAaddra),  // input  wire [10 : 0] addra
   .dina (0      ),  // input  wire [17 : 0] dina
   .douta(LAdouta),  // output wire [17 : 0] douta
   .clkb (clk    ),  // input  wire          clkb
   .web  (LAweb  ),  // input  wire [0  : 0] web
   .addrb(LAaddrb),  // input  wire [10 : 0] addrb
   .dinb (LAdinb ),  // input  wire [17 : 0] dinb
   .doutb(       )   // output wire [17 : 0] doutb
  );
   
  
endmodule