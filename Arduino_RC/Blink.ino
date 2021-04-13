#include <SoftwareSerial.h>
#include <Servo.h>
#define DEBUG true 
#define BT_RXD 2 
#define BT_TXD 3 
SoftwareSerial ESP_wifi(BT_RXD, BT_TXD);
Servo servo;
int servo_angle = 90;

int RightMotor_E_pin = 5;       // 오른쪽 모터의 Enable & PWM
int LeftMotor_E_pin = 6;        // 왼쪽 모터의 Enable & PWM
int RightMotor_1_pin = 8;       // 오른쪽 모터 제어선 IN1
int RightMotor_2_pin = 9;       // 오른쪽 모터 제어선 IN2
int LeftMotor_3_pin = 10;       // 왼쪽 모터 제어선 IN3
int LeftMotor_4_pin = 11;       // 왼쪽 모터 제어선 IN4

int motor_s = 145;              // 최대 속도(0~255)의 60% 

int R_Motor = 0;
int L_Motor = 0;
int mode = 0;

String income_wifi=""; 
String ssid = "jji";
String password = "ji201533668";

String sendData(String command, const int timeout, boolean debug) {
  String response = "";
  ESP_wifi.print(command); // send the read character to the esp01
  long int time = millis();
  while( (time+timeout) > millis()) {
    while(ESP_wifi.available()) {  // The esp has data so display its output to the serial window 
      char c = ESP_wifi.read(); // read the next character.
      response += c;
    }
  }
  if(debug) Serial.print(response);
  return response;
}
void control(String Blue_val) {
  if( Blue_val == "up" ){      //  명령 : 속도 증가
        motor_s = motor_s + 20;
        motor_s = min(motor_s, 255);
        Serial.print("Speed Up : "); 
      }
  
      else if( Blue_val == "down" ){ //  명령 : 속도 감소
      motor_s = motor_s - 20;
      motor_s = max(motor_s, 50);
      Serial.print("Speed Down : ");
     }
  
      else if( Blue_val == "GO" ){  //  명령 : 전진
      R_Motor = HIGH; L_Motor = HIGH;
      motor_role(R_Motor, L_Motor, motor_s);
    }  
  
      else if( Blue_val == "LEFT" ){ //  명령 : 좌회전
      Left_role(R_Motor, L_Motor, motor_s);
    }
  
      else if( Blue_val == "RIGHT" ){ //  명령 : 우회전
      Right_role(R_Motor, L_Motor, motor_s);
    }
  
      else if( Blue_val == "TURN" ){ //  명령 : 후진
      R_Motor = LOW;
      L_Motor = LOW;
      motor_role(R_Motor, L_Motor, motor_s);
    }

      else if( Blue_val == "STOP" ){ //  명령 : 정지
      motor_role(R_Motor, L_Motor, 0);
    }

      else if( Blue_val == "Camera_LEFT" ){ //  명령 : 카메라 왼쪽
        servo.write(180);
        delay(2000);
        Serial.println(180);
    }

      else if( Blue_val == "Camera_RIGHT" ){ //  명령 : 카메라 오른쪽
        servo.write(0);
        delay(2000);
        Serial.println(0);
    }
     
     else if( Blue_val == "Camera_CENTER" ){ //  명령 : 카메라 오른쪽
        servo.write(90);
        delay(2000);
        Serial.println(0);
    }
  else{
    Serial.println(Blue_val);
  }
}
void setup() { 
pinMode(RightMotor_E_pin, OUTPUT);        // 출력모드로 설정
pinMode(RightMotor_1_pin, OUTPUT);
pinMode(RightMotor_2_pin, OUTPUT);
pinMode(LeftMotor_3_pin, OUTPUT);

//Servo
pinMode(9, OUTPUT);
servo.attach(9);

pinMode(LeftMotor_4_pin, OUTPUT);
pinMode(LeftMotor_E_pin, OUTPUT);
Serial.begin(9600); 
ESP_wifi.begin(9600);
 sendData("AT+RST\r\n",2000,DEBUG); // reset module
  sendData("AT+CWMODE=1\r\n",1000,DEBUG); // configure as access point (working mode: AP+STA)
  //sendData("AT+CWDHCP=1,1\r\n",1000,DEBUG);
  sendData("AT+CWJAP=\""+ ssid +"\",\""+password+"\"\r\n",8000,DEBUG);
  sendData("AT+CIFSR\r\n",1000,DEBUG); // get ip address
  sendData("AT+CIPMUX=1\r\n",1000,DEBUG); // configure for multiple connections
  sendData("AT+CIPSERVER=1,2000\r\n",1000,DEBUG); // turn on server on port 79
}

void loop() {  
if (Serial.available()){
 ESP_wifi.write(Serial.read()); 
} 
if (ESP_wifi.available()) {
if (ESP_wifi.find("+IPD,")) {
      income_wifi = ESP_wifi.readStringUntil('\r');
      String Blue_val = income_wifi.substring(income_wifi.indexOf("GET /")+5, income_wifi.indexOf("HTTP/1.1")-1);
      control(Blue_val);
    }
  }
}
void motor_role(int R_motor, int L_motor, int Speed){
   digitalWrite(RightMotor_1_pin, R_motor);
   digitalWrite(RightMotor_2_pin, !R_motor);
   digitalWrite(LeftMotor_3_pin, L_motor);
   digitalWrite(LeftMotor_4_pin, !L_motor);
   
   analogWrite(RightMotor_E_pin, Speed);  // 우측 모터 속도값
   analogWrite(LeftMotor_E_pin, Speed);   // 좌측 모터 속도값  
}

void Right_role(int R_motor, int L_motor, int Speed){
   digitalWrite(RightMotor_1_pin, R_motor);
   digitalWrite(RightMotor_2_pin, !R_motor);
   digitalWrite(LeftMotor_3_pin, L_motor);
   digitalWrite(LeftMotor_4_pin, !L_motor);
   
   analogWrite(RightMotor_E_pin, max(Speed*0.4,50));  // 우측 모터 속도값
   analogWrite(LeftMotor_E_pin, min(Speed*1.4,255));   // 좌측 모터 속도값
}

void Left_role(int R_motor, int L_motor, int Speed){
   digitalWrite(RightMotor_1_pin, R_motor);
   digitalWrite(RightMotor_2_pin, !R_motor);
   digitalWrite(LeftMotor_3_pin, L_motor);
   digitalWrite(LeftMotor_4_pin, !L_motor);
   
   analogWrite(RightMotor_E_pin, min(Speed*1.4,255));  // 우측 모터 속도값
   analogWrite(LeftMotor_E_pin, max(Speed*0.2,50));   // 좌측 모터 속도값   
}
