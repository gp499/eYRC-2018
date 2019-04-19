/*
 * Team Id: 1753
 * Author list: Guruprasad Bhat, Anjaneya Ketkar, Sankirthana Saraswatula, Nilesh Gandhi
 * Filename: Thirsty_Crow.c
 * Theme: Thirsty Crow

 * Functions: magnet_pin_config(),motor_pin_config(),adc_pin_config(void),uart0_init(), uart_rx(),uart_tx(char data) adc_init(),timer5_init(), velocity (unsigned char left_motor, unsigned char right_motor),void motion_set (unsigned char Direction),char ADC_Conversion(unsigned char Ch),magnet_on(),void magnet_off(),forward (),backward(),left(),right(),soft_left(),soft_right().buzz(),stop(),SIGNAL(SIG_USART0_RECV),motion_set (unsigned char Direction), magnet_on(), magnet_off(), forward (), backward (), left (), right (),void init_devices (),int main(void)soft_left (), soft_right (), stop (), init_devices (),

 *Global Variables: F_CPU, RX  (1<<4),TX  (1<<3),TE  (1<<5),RE  (1<<7), data, ADC_Conversion(unsigned char),ADC_Value, flag = 0,Left_white_line ,Center_white_line Right_white_line, count;			  
 * 
 */ 




#define F_CPU 14745600
#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>
#define RX  (1<<4)
#define TX  (1<<3)
#define TE  (1<<5)
#define RE  (1<<7)
volatile unsigned int data;
unsigned char ADC_Conversion(unsigned char);
unsigned char ADC_Value;
volatile unsigned char flag = 0;
unsigned char Left_white_line = 0;
unsigned char Center_white_line = 0;
unsigned char Right_white_line = 0;
volatile uint8_t count=0;


/*
* Function Name:magnet_pin_config
* Input: None
* Output: None
* Logic: Setting up pin H0 for output (electromagnet)
* Example Call:  magnet_pin_config()
*/

void magnet_pin_config()
{
	DDRH = 0x01 ;  //enabling H0 as output
	PORTH = 0x00;  //setting Pins as LOW
}


/*
* Function Name:motor_pin_config
* Input: None
* Output: None
* Logic: Setting pins A0,A1,A2,A3, L3,L4(Motor pins with 2 pwm pins)
* Example Call: motor_pin_config()
*/
void motor_pin_config()
{
	DDRA = 0x0F ;
	PORTA = 0x00;
	DDRL = DDRL | 0x18;   //Setting PL3 and PL4 pins as output for PWM generation
	PORTL = PORTL | 0x18; //PL3 and PL4 pins are for velocity control using PWM.
}


/*
* Function Name:adc_pin_config
* Input: None
* Output: none
* Logic: Setting pins  of port F for white line sensors
* Example Call: adc_pin_config ()
*/

void adc_pin_config (void)
{
	DDRF = 0x00; //set PORTF direction as input
	PORTF = 0x00; //set PORTF pins floating
}


/*
* Function Name:uart0_init()
* Input: None
* Output: none
* Logic: Setting up uart communication at usart0 for x bee communication with baud rate 9600 
	
* Example Call: uart0_init()
*/

void uart0_init()
{
	UCSR0B = 0x00;							//disable while setting baud rate
	UCSR0A = 0x00;
	UCSR0C = 0x06;
	UBRR0L = 0x5F; 							//9600BPS at 14745600Hz
	UBRR0H = 0x00;
	UCSR0B = 0x98;
	//UCSR0C = 3<<1;							//setting 8-bit character and 1 stop bit
	//UCSR0B = RX | TX;
}


/*
* Function Name:timer5_init
* Input: None
* Output: None
* Logic: Setting up compare registers for both motors and timer
* Example Call: timer5_init()
*/
void timer5_init()
{
	TCCR5B = 0x00;	//Stop
	TCNT5H = 0xFF;	//Counter higher 8-bit value to which OCR5xH value is compared with
	TCNT5L = 0x01;	//Counter lower 8-bit value to which OCR5xH value is compared with
	OCR5AH = 0x00;	//Output compare register high value for Left Motor
	OCR5AL = 0xFF;	//Output compare register low value for Left Motor
	OCR5BH = 0x00;	//Output compare register high value for Right Motor
	OCR5BL = 0xFF;	//Output compare register low value for Right Motor
	OCR5CH = 0x00;	//Output compare register high value for Motor C1
	OCR5CL = 0xFF;	//Output compare register low value for Motor C1
	TCCR5A = 0xA9;
	TCCR5B = 0x0B;	//WGM12=1; CS12=0, CS11=1, CS10=1 (Prescaler=64)
}


/*
* Function Name:adc_init()
* Input: None
* Output: none
* Logic: initialising adc channels
* Example Call: adc_init()
*/
void adc_init()
{
	ADCSRA = 0x00;
	ADCSRB = 0x00;		//MUX5 = 0
	ADMUX = 0x20;		//Vref=5V external --- ADLAR=1 --- MUX4:0 = 0000
	ACSR = 0x80;
	ADCSRA = 0x86;		//ADEN=1 --- ADIE=1 --- ADPS2:0 = 1 1 0
}


/*
* Function Name:ADC_Conversion
* Input: analog value of channel  
* Output: digital value of the channel mapped to 255
* Logic: Converting to digital value of analog sensors using adc
* Example Call: ADC_Conversion( Ch)
*/

unsigned char ADC_Conversion(unsigned char Ch)
{
	unsigned char a;
	if(Ch>7)
	{
		ADCSRB = 0x08;
	}
	Ch = Ch & 0x07;
	ADMUX= 0x20| Ch;
	ADCSRA = ADCSRA | 0x40;		//Set start conversion bit
	while((ADCSRA&0x10)==0);	//Wait for ADC conversion to complete
	a=ADCH;
	ADCSRA = ADCSRA|0x10; //clear ADIF (ADC Interrupt Flag) by writing 1 to it
	ADCSRB = 0x00;
	return a;
}



/*
* Function Name:uart_rx
* Input: none 
* Output: returns the received value
* Logic: Waits for the user to input values and returns recieved value
* Example Call: uart_rx()
*/
char uart_rx()
{
	while(!(UCSR0A & RE));						//waiting to receive
	return UDR0;
}



/*
* Function Name:uart_tx
* Input:data to be transmitted to the user 
* Output: none
* Logic: Waits transmission and transmits data 
* Example Call: uart_tx()
*/
void uart_tx(char data)
{
	while(!(UCSR0A & TE));						//waiting to transmit
	UDR0 = data;
}


/*
* Function Name:velocity 
* Input: value ranging upto 255 for setting up maximum speed for both motors 
* Output: None
* Logic: controls max value for  each motor i.e speed of motor can be mapped to particular value
* Example Call: velocity (unsigned char left_motor, unsigned char right_motor)
*/
void velocity (unsigned char left_motor, unsigned char right_motor)
{
	OCR5AL = (unsigned char)left_motor;
	OCR5BL = (unsigned char)right_motor;
}

/*
* Function Name:motion_set 
* Input: Values to specify direction (HEX values giving which motors to be operated for particular direction)
* Output: None
* Logic: Given values will make the particular registers HIGH giving the appropiate direction for both motors
* Example: motion_set (unsigned char Direction) 
*/
void motion_set (unsigned char Direction)
{
	unsigned char PortARestore = 0;

	Direction &= 0x0F; 			// removing upper nibbel as it is not needed
	PortARestore = PORTA; 			// reading the PORTA's original status
	PortARestore &= 0xF0; 			// setting lower direction nibbel to 0
	PortARestore |= Direction; 	// adding lower nibbel for direction command and restoring the PORTA status
	PORTA = PortARestore; 			// setting the command to the port
}



/*
* Function Name:magnet_on
* Input: None
* Output: None
* Logic: Makes pin H0 HIGH(for making magnet on)
* Example Call: magnet_on()
*/

void magnet_on()
{
	PORTH = 0x01 ;
}


/*
* Function Name:magnet_off
* Input: None
* Output: None
* Logic:Makes pin H0 LOW(making magnet off)
* Example Call: magnet_off()
*/

void magnet_off()
{
	PORTH = 0x00;
}


/*
* Function Name:forward 
* Input: None
* Output: None
* Logic: both wheels forward
* Example Call: forward ()
*/

void forward ()
{
	motion_set(0x06);
}



/*
* Function Name:backward 
* Input: None
* Output: None
* Logic: both wheels backward
* Example Call: backward ()
*/
void backward ()
{
	motion_set(0x09);
}



/*
* Function Name:left
* Input: None
* Output: None
* Logic: Left wheel backward, Right wheel forward
* Example Call: left ()
*/
void left ()
{
	motion_set(0x05);
}



/*
* Function Name:right 
* Input: None
* Output: None
* Logic: Left wheel forward, Right wheel backward
* Example Call: right ()
*/
void right ()
{
	motion_set(0x0A);
}


/*
* Function Name:soft_left 
* Input: None
* Output: None
* Logic: Left wheel stationary, Right wheel forward
* Example Call: soft_left () 
*/

void soft_left ()
{
	motion_set(0x04);
}

/*
* Function Name:soft_right 
* Input: None
* Output: None
* Logic: Left wheel forward, Right wheel is stationary
* Example Call: soft_right ()
*/
void soft_right ()
{
	motion_set(0x02);
}



/*
* Function Name:stop 
* Input: None
* Output: None
* Logic: stops both wheels
* Example Call: stop ()
*/
void stop ()
{
	motion_set(0x00);
}


/*
* Function Name:buzz_config
* Input: None
* Output: None
* Logic: Setting up B0 as output for buzzer 
* Example Call: buzz_config()
*/
void buzz_config(){
	DDRB=0X00;
	PORTB=0X00;
}

/*
* Function Name:buzz
* Input: None
* Output: None
* Logic: buzzer buzzes 
* Example Call: buzz()
*/
void buzz()
{
	PORTB=0X01;
	_delay_ms(5000);
	PORTB=0X00;
	_delay_ms(1000);
}


/*
* Function Name:SIGNAL
* Input: data received from the user  
* Output: None
* Logic: interrupt  
* Example Call: called whenever interrupt occurs
*/

SIGNAL(SIG_USART0_RECV) 		// ISR for receive complete interrupt
{
	data = UDR0; 				//making copy of data from UDR0 in 'data' variable
	UDR0 = data; 				//echo data back to PC
	
	if(data == 'l') //left from node
	{
		forward();
		velocity(100,110);
		_delay_ms(300);
		left();
		velocity(90,120);
		_delay_ms(135); 
	}

	if(data == 'r') //right from node
	{
		forward();
		velocity(100,110);
		_delay_ms(300);
		right();
		velocity(120,90);
		_delay_ms(135); 
	}
	if (data=='p')//reached pebble/pitcher
	{
		forward();
		velocity(100,110);
		_delay_ms(1300);
		stop();		//Alternate picking and dropping of pebbles whenever 'p' is recieved		
		if (flag %2== 0){
			magnet_on();
			flag++;
		}
		else{
			magnet_off();
			flag++;
			count++;
		}
		_delay_ms(1000);
		backward();
		velocity(100,110);
		_delay_ms(1250);
		if (count==3){  //After 3 pickups and drops ... buzzer to be sounded for 5 secs
			stop();
			buzz();
			
		}					
	}
	if (data=='u'){
		left();
		velocity(150,150);
		_delay_ms(470);
	}
}



/*
* Function Name:init_devices
* Input: None
* Output: None
* Logic: to initialize all devices
* Example Call: init_devices () 
*/
void init_devices ()
{
	cli(); //disable all interrupts
	motor_pin_config();
	adc_pin_config();
	buzz_config();
	magnet_pin_config();
	timer5_init();
	uart0_init();
	adc_init();
	sei(); //re-enable interrupts
}


/*
* Function Name:main
* Input: None
* Output: int to inform the caller that the program exited correctly or Incorrectly 
* Logic: Set velocity for both wheels(using pwm) , Make bot go Forward 3 secs, Magnetise, Backward 3 secs and Demagnetise 
* Example Call: Automatically called by OS
*/


int main(void)
{
	init_devices();
	velocity (100, 100);//Set robot velocity here
	while (1)
	{
		Left_white_line = ADC_Conversion(3);	//Getting data of Left WL Sensor
		Center_white_line = ADC_Conversion(2);	//Getting data of Center WL Sensor
		Right_white_line = ADC_Conversion(1);	//Getting data of Right WL Sensor
		//data=uart_rx();	
	//Goes Straight checking conditions of the 3 white line sensor values
	if((Center_white_line>0x28) && (Left_white_line<0x37) && (Right_white_line<0x37) )
	{
		forward();
		velocity(150,165);
	}
	//reverse when white
	if((Center_white_line<0x28) && (Left_white_line<0x28) && (Right_white_line<0x28) )
	{
		backward();
		velocity(100,110);
		_delay_ms(100);
	}
	//slight right for better line following
	if(((Left_white_line>0x28) && (Right_white_line<0x28)&&(Center_white_line>0x28))||((Left_white_line>0x28) && (Right_white_line<0x28)&&(Center_white_line<0x28)))
	{
		forward();
		velocity(150,66);
	}
	//slight left for better line following
	if(((Right_white_line<0x28) && (Center_white_line>0x28) && (Left_white_line<0x28))||((Right_white_line>0x28) && (Center_white_line<0x28) && (Left_white_line<0x28)))
	{

		forward();
		velocity(66,150);
	}
	//reached a node 
	if((Center_white_line>0x28) && (Left_white_line>0x28) && (Right_white_line>0x28))
	{
		stop();
		uart_tx('n');	//Transmit 'n' to let the python know that it has reached a node 
		_delay_ms(2000);	
	}
	}
}

