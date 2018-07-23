`timescale 1ns / 1ps
`define WH1920x1080 3
`define WH1280x1024 0

module Top(
  input               sys_clk,
  output			        vga_hs,		   //horizontal sync 
  output			        vga_vs,		   //vertical sync
  output  [4:0]	      vga_r,		   //VGA R data
  output	[5:0]	      vga_g,		   //VGA G data
  output	[4:0] 	    vga_b,		   //VGA B data
  input               key1,
  input               key2,
  input               key3,
  input               key4,
  
  output              e_reset,
  //output               e_mdc,                      //MDIO的时钟信号，用于读写PHY的寄存器 
  //inout                e_mdio,                     //MDIO的数据信号，用于读写PHY的寄存器	
  input	               e_rxc,                      //125Mhz ethernet gmii rx clock
	input	               e_rxdv,	                   //GMII 接收数据有效信号
	input	               e_rxer,	                   //GMII 接收数据错误信号					
	input      [7:0]     e_rxd,                      //GMII 接收数据	      

	input	               e_txc,                      //25Mhz ethernet mii tx clock         
	output               e_gtxc,                     //125Mhz ethernet gmii tx clock  
	output               e_txen,                     //GMII 发送数据有效信号	
	output               e_txer,                     //GMII 发送数据错误信号					
	output     [7:0]     e_txd	                      //GMII 发送数据 	
  
  
  );
  wire [11:0] X_5,Y,Width,Height;
  wire [7 :0] R,G,B,RO,GO,BO;  
  
  assign e_gtxc = e_rxc;	 
  assign e_reset = 1'b1; 
  
  assign vga_r = RO[7:3],
         vga_g = GO[7:2],
         vga_b = BO[7:3];
  
  assign SendEn = !key3Reg[1] && key3Reg[2];  
  assign ClearMac = !key1Reg[1] && key1Reg[2]; 
  
  wire  CLK_VGA = CLK_107;
  
  wire [10:0] Ram_MacText_addr;
  wire [8 :0] Ram_MacText_din; 
  wire [23:0] TxCNT,RxCNT,TxLimit;
  wire [15:0] Data_Length,Gapength;
  wire [7 :0] FrameRate;
  Mac_Ctrl iMac_Ctrl(
    .clk             (e_rxc),
    .TxEn            (e_txen),
    .TxErr           (e_txer),
    .TxData          (e_txd),
    .RxEn            (e_rxdv),
    .RxData          (e_rxd),
    .SendEn          (SendEn),
    .Dkey2           (!key2Reg[2]),
    .Clear           (ClearMac),
    .DataLength     (Data_Length),
    .GapLength       (GapLength),
    .TxCNT           (TxCNT),
    .RxCNT           (RxCNT),
    .TxLimit         (TxLimit),
    .FrameRate       (FrameRate),
    .Ram_MacText_we  (Ram_MacText_we),
    .Ram_MacText_addr(Ram_MacText_addr),
    .Ram_MacText_din (Ram_MacText_din),
    .Ram_MacText_dout(0)
);
  
  VGA_HDMI iVGA_HDMI(
    .clk          (CLK_VGA),
    .Vsync        (vga_vs),
    .Hsync        (vga_hs),
    .DataEn       (),
    .X            (),
    .X_5          (X_5),
    .Y            (Y),
    .Width        (Width),
    .Height       (Height),
    .ResolutionSel(`WH1280x1024),
    .RGBI_R       (R),
    .RGBI_G       (G),
    .RGBI_B       (B),
    .RGBO_R       (RO),
    .RGBO_G       (GO),
    .RGBO_B       (BO)
    );
  KeyDetect (
    .clk  (CLK_VGA),
    .key1 (key1 ),
    .key2 (key2 ),
    .key3 (key3 ),
    .key4 (key4 ),
    .Dkey1(Dkey1),
    .Dkey2(Dkey2),
    .Dkey3(Dkey3),
    .Dkey4(Dkey4),
    .Clear(Clear),
    .Dkey1Down(Dkey1Down)
  );  
    
  
  wire [11:0] TextBox0_Ram_addr;
  wire [8 :0] TextBox0_Ram_dout;  
  wire [10:0] Char0_Rom_addr;
  wire [15:0] Char0_Rom_dout;
  FPGA_GUI iFPGA_GUI(
    .clk   (CLK_VGA),
    .X_5   (X_5),
    .Y     (Y),
    .Width (Width),
    .Height(Height),
    .Clear(Clear),
    .Dkey1Down(Dkey1Down),
    .Arbiter0_RGBO_R(R),
    .Arbiter0_RGBO_G(G),
    .Arbiter0_RGBO_B(B),
    .Char0_Rom_we     (),
    .Char0_Rom_addr   (Char0_Rom_addr),
    .Char0_Rom_din    (),
    .Char0_Rom_dout   (Char0_Rom_dout),
    .TextBox0_Ram_we  (TextBox0_Ram_we),
    .TextBox0_Ram_addr(TextBox0_Ram_addr),
    .TextBox0_Ram_din (),
    .TextBox0_Ram_dout(TextBox0_Ram_dout)  
    
  );
 
 
  reg [2 :0] key3Reg = 1,key2Reg = 1,key1Reg = 1;    
  reg [10:0] TRaddrb = 0; 
  reg  TRweb;
  
  always@(posedge e_rxc)
  begin 
  	key3Reg[0] <= Dkey3;
  	key3Reg[2:1] <= key3Reg[1:0];   
  	key2Reg[0] <= Dkey2;         
  	key2Reg[2:1] <= key2Reg[1:0];   
  	key1Reg[0] <= Dkey1;         
  	key1Reg[2:1] <= key1Reg[1:0];
  	//TRweb <= !key2Reg[1] && key2Reg[2];
  	//if(TRweb)
  	//  TRaddrb <= TRaddrb + 1;
  	//else if(Clear)
  	//  TRaddrb <= 0;
  	
  end
  
  
  TextRam9x2048 iTextRam9x2048 (
    .clka(CLK_VGA), // input clka
    .wea(TextBox0_Ram_we), // input [0 : 0] wea
    .addra(TextBox0_Ram_addr), // input [10 : 0] addra
    .dina(0), // input [8 : 0] dina
    .douta(TextBox0_Ram_dout), // output [8 : 0] douta
    .clkb (e_rxc),//(CLK_VGA     ), // input clkb
    .web  (Ram_MacText_we),//(TRweb       ), // input [0 : 0] web
    .addrb(Ram_MacText_addr),//(TRaddrb     ), // input [10 : 0] addrb
    .dinb (Ram_MacText_din),//({0,X_5[6:0]}), // input [8 : 0] dinb
    .doutb() // output [8 : 0] doutb
   );  
    

   
   
   FontRam16x2048  iFontRam16x2048(
    .clka(CLK_VGA), // input clka
    .wea(0), // input [0 : 0] wea
    .addra(Char0_Rom_addr), // input [10 : 0] addra
    .dina(0), // input [15 : 0] dina
    .douta(Char0_Rom_dout), // output [15 : 0] douta
    .clkb(CLK_VGA), // input clkb
    .web(0), // input [0 : 0] web
    .addrb(0), // input [10 : 0] addrb
    .dinb(0), // input [15 : 0] dinb
    .doutb() // output [15 : 0] doutb
   );
  
  /*
  PLL1 iPLL1
   (// Clock in ports
    .CLK_IN1(sys_clk),      // IN
    // Clock out ports
    .CLK_100(CLK_100),     // OUT
    .CLK_125(CLK_125),     // OUT
    .CLK_142(CLK_142),     // OUT
    .CLK_111(CLK_111));    // OUT
  */
  PLL2 iPLL2
   (// Clock in ports
    .CLK_IN1(sys_clk),      // IN
    // Clock out ports
    .CLK_150(CLK_150),     // OUT
    .CLK_107(CLK_107),     // OUT
    .CLK_50(CLK_50));    // OUT  
  wire [35:0] CONTROL0,CONTROL1;
  wire [127:0] SYNC_IN,SYNC_OUT;
  reg        RxReg ;
  reg [7:0]  RxData;   
  wire [7:0] TRIG0;
  always@(posedge e_rxc)
  begin
  	RxReg  <= e_rxdv;
  	RxData <= e_rxd ;
  end
  
  /*
  ICON1 iICON1 (
    .CONTROL0(CONTROL0) // INOUT BUS [35:0]
  );*/
  ICON2 iICON2 (                    
      .CONTROL0(CONTROL0), // INOUT BUS [35:0]
      .CONTROL1(CONTROL1) // INOUT BUS [35:0] 
  );                                          
  
  VIO1 iVIO1 (
    .CONTROL(CONTROL0), // INOUT BUS [35:0]
    .CLK(e_rxc), // IN
    .SYNC_IN(SYNC_IN), // IN BUS [127:0]
    .SYNC_OUT(SYNC_OUT) // OUT BUS [127:0]
  );
  
  ILA1 iILA1 (                   
      .CONTROL(CONTROL1), // INOUT BUS [35:0]
      .CLK(e_rxc), // IN                      
      .DATA({RxReg,RxData}), // IN BUS [8:0]          
      .TRIG0(TRIG0) // IN BUS [7:0]         
  );                                        
  assign SYNC_IN = {0,
                    FrameRate, //48 63
                    TxCNT,  //24 47
						  RxCNT}; //0 23
  assign Data_Length = SYNC_OUT[15:0];
  assign GapLength = SYNC_OUT[31:16]; 
  assign TxLimit = SYNC_OUT[55:32]; 
  assign TRIG0 = {0,e_txen,e_rxdv};
  
endmodule