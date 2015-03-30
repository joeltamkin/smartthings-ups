/**
 *  UPS
 *
 *  Copyright 2015 Joel Tamkin
 *
 *  Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
 *  in compliance with the License. You may obtain a copy of the License at:
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
 *  on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License
 *  for the specific language governing permissions and limitations under the License.
 *
 */
metadata {
     definition (name: "UPS", author: "Joel Tamkin") {
          capability "Alarm"
          capability "Battery"
          capability "Contact Sensor"
          capability "Power Meter"
          capability "Temperature Measurement"
          capability "Switch"
          capability "Sensor"

          attribute "input_voltage", "string"
          attribute "input_current", "string"
          attribute "input_frequency", "string"
          attribute "input_state", "string"
	  attribute "output_voltage", "string"
	  attribute "output_current", "string"
          attribute "output_power", "string"
          attribute "output_percent", "string"
          attribute "output_source", "string"

          attribute "battery_percent", "string"
	  attribute "battery_timeremaining", "string"
	  attribute "battery_voltage", "string"

          attribute "system_temperature", "string"
          attribute "system_alarm", "string"

          attribute "system_status", "string"

          command "silenceAlarm"
          command "setStatus"
          command "setPoints"
          }

	simulator {
		// TODO: define status and reply messages here

	}

     tiles {
          standardTile("status", "device.system_status", canChangeBackground: true, canChangeIcon: true) {
               state "normal", label:'NORMAL', icon: "st.Appliances.appliances17", backgroundColor: "#79b821"
               state "onbattery", label:"ON BATTERY", icon: "st.Appliances.appliances17", backgroundColor: "#f5b220"
               state "onbypass", label:"ON BYPASS", icon: "st.Appliances.appliances17", backgroundColor: "#f5b220"
               state "manualoff", label:"MANUAL OFF", icon: "st.Appliances.appliances17", backgroundColor: "#0000FF"
               state "fail", label:"FAILURE", icon: "st.Appliances.appliances17", backgroundColor: "#FF0000"
               }

          valueTile("inputvoltage", "device.input_voltage", width: 1, height: 1) {
               state("input_voltage", label:' INPUT: ${currentValue} VAC',
               backgroundColors:[
                [value: 114, color: "#ff0000"],
                [value: 115, color: "#ff3b0b"],
                [value: 116, color: "#fa7616"],
                [value: 117, color: "#f5b220"],
                [value: 118, color: "#f1d801"],
                [value: 119, color: "#b5c811"],
                [value: 120, color: "#79b821"],
                [value: 122, color: "#79b821"],
                [value: 123, color: "#79b821"],
                [value: 124, color: "#79b821"],
                [value: 125, color: "#79b821"],
                [value: 126, color: "#b5c811"],
                [value: 127, color: "#f1d801"],
		[value: 128, color: "#f5b220"],
                [value: 129, color: "#ff0000"]
                ])
               }

        standardTile("inputstate", "device.input_state", canChangeBackground: false, canChangeIcon: false) {
             state "ok",   label:'INPUT OK', icon: "st.switches.switch.on",   backgroundColor: "#79b821"
      	     state "bad", label:'INPUT BAD', icon: "st.switches.switch.off", backgroundColor: "#ff0000"
        }
        
        valueTile("inputfreq", "device.input_frequency", width: 1, height: 1) {
        state("input_frequency", label:'${currentValue} Hz',
            backgroundColors:[
                [value: 57, color: "#ff0000"],
                [value: 58, color: "#ff3b0b"],
                [value: 59, color: "#f1d801"],
                [value: 60, color: "#79b821"],
                [value: 61, color: "#f1d801"],
            ]
        )}
        
        valueTile("outputvoltage", "device.output_voltage", width: 1, height: 1) {
        state("output_voltage", label:'OUTPUT: ${currentValue} VAC',
            backgroundColors:[
                [value: 114, color: "#ff0000"],
                [value: 115, color: "#ff3b0b"],
                [value: 116, color: "#fa7616"],
                [value: 117, color: "#f5b220"],
                [value: 118, color: "#f1d801"],
                [value: 119, color: "#b5c811"],
                [value: 120, color: "#79b821"],
                [value: 122, color: "#79b821"],
                [value: 123, color: "#79b821"],
                [value: 124, color: "#79b821"],
                [value: 125, color: "#79b821"],
                [value: 126, color: "#b5c811"],
                [value: 127, color: "#f1d801"],
				[value: 128, color: "#f5b220"],
                [value: 129, color: "#ff0000"]
            ]
        )}
        standardTile("outputsource", "device.output_source", canChangeBackground: false, canChangeIcon: false) {
      	state "normal", label:'OUTPUT OK', action: "off", icon: "st.switches.switch.on",   backgroundColor: "#79b821"
      	state "none", label:'OUTPUT OFF', action: "on", icon: "st.switches.switch.off", backgroundColor: "ff0000"
        state "bypass", label:'IN BYPASS', action: "on", icon: "st.switches.switch.off", backgroundColor: "#f5b220"
        state "battery", label:'ON BATTERY', icon: "st.switches.switch.off", backgroundColor: "#F6EF1F"
        }
        
        valueTile("loadpercent", "device.output_percent", width: 1, height: 1) {
        state("output_percent", label:'${currentValue}% VA',
            backgroundColors:[
                [value: 25, color: "#79b821"],
                [value: 35, color: "#b5c811"],
                [value: 45, color: "#f1d801"],
                [value: 55, color: "#f5b220"],
                [value: 65, color: "#fa7616"],
                [value: 75, color: "#ff3b0b"],
                [value: 85, color: "#ff0000"]
            ]
        )}
               
        valueTile("battery", "device.battery_percent", width: 1, height: 1) {
        state("battery_percent", label:'BATT ${currentValue}%',
            backgroundColors:[
                [value: 25, color: "#ff0000"],
                [value: 45, color: "#ff3b0b"],
                [value: 60, color: "#fa7616"],
                [value: 75, color: "#f5b220"],
                [value: 85, color: "#f1d801"],
                [value: 90, color: "#b5c811"],
                [value: 95, color: "#79b821"]
            ]
        )}
        valueTile("temperature", "device.system_temperature", width: 1, height: 1) {
        state("system_temperature", label:'${currentValue}°F',
            backgroundColors:[
                [value: 31, color: "#153591"],
                [value: 44, color: "#1e9cbb"],
                [value: 59, color: "#90d2a7"],
                [value: 74, color: "#44b621"],
                [value: 84, color: "#f1d801"],
                [value: 95, color: "#d04e00"],
                [value: 96, color: "#bc2323"]
            ]
        )}
        valueTile("power", "device.output_power", width: 1, height: 1) {
        state("output_power", label:'${currentValue} Watts',
            backgroundColor: "#444444"
        )}
        
        standardTile("alarm", "device.system_alarm", canChangeBackground: false, canChangeIcon: false, width: 3, height: 1) {
      	state "alarm",   label:'ALARM', action: "silenceAlarm", icon: "st.alarm.beep.beep",   backgroundColor: "#ff0000"
      	state "ok", label:'SYSTEM OK', icon: "st.alarm.beep.beep", backgroundColor: "#79b821"
        }
        
        // This tile will be the tile that is displayed on the Hub page.
    	main "status"

    	// These tiles will be displayed when clicked on the device, in the order listed here.
    	details(["alarm", "inputvoltage", "inputfreq", "inputstate", "temperature", "power", "battery", "outputvoltage", "loadpercent", "outputsource"])
	}
}

// parse events into attributes
def parse(String description) {
	log.debug "Parsing '${description}'"

  	def myValues = description.tokenize()

  	// log.debug "Description: ${myValues[0..-1]} - ${myValues[-1]}"
    
  	//sendEvent (name: "${myValues[0..-1]}", value: "${myValues[-1]}") 
}


// handle commands

def on() {
}

def off() {
}

def setStatus(String description) {
	log.debug "setstatus '${description}'"

  	def myValues = description.tokenize()

  	log.debug "Description: ${myValues[0]} - ${myValues[1]}"
    
    switch (myValues[0]) {
    	case "system_temperature":
        	sendEvent (name: "temperature", value: "${myValues[1]}")
            break
        case "output_power":
        	sendEvent (name: "power", value: "${myValues[1]}")
            break
        case "battery_percent":
        	sendEvent (name: "battery", value: "${myValues[1]}")
            break
        case "system_alarm":
        	switch(myValues[1]) {
            	case "ok":
                	sendEvent (name: "status", value: "ok")
                    break
                case "alarm":
                	sendEvent (name: "status", value: "alarm")
            	    break
                }    
        case "output_source":
        	switch(myValues[1]) {
            	case "bypass":
                	sendEvent (name: "system_status", value: "onbypass")
                    break
                case "battery":
                	sendEvent (name: "system_status", value: "onbattery")
                    break
                case "none":
                	sendEvent (name: "system_status", value: "manualoff")
                    break
                case "normal":
                	sendEvent (name: "system_status", value: "normal")
                    break 
                }
            break          
         }
    
  	sendEvent (name: "${myValues[0]}", value: "${myValues[1]}") 
}

def setPoints(points) {
    log.debug "device.setPoints: ${points}"
    points.each { setStatus("$it.key $it.value") }
}

def silenceAlarm() {
    log.debug "Executing 'silenceAlarm'"
    // TODO: handle 'silenceAlarm' command
}


