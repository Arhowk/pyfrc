import pygame
import logging
logger = logging.getLogger("joysticks")

class UsbJoysticks(object):
    
    def __init__(self, ui):
        pygame.init()
        
        self.ui = ui
        
        self.joysticks = self.getUsbJoystickList()
        self.initJoystickList(self.joysticks)
        
    def getUsbJoystickList(self):
        joysticks = []
        
        for i in range(pygame.joystick.get_count()):
            joysticks.append(pygame.joystick.Joystick(i))
            

                
        return joysticks
    
    def initJoystickList(self, joystickList):
        i = 0;
        for joystick in joystickList:
            joystick.init()
            if joystick.get_numaxes() == 5:
                logger.info("Joystick {} reporting as an Xbox Controller".format(i))
            i = i + 1
        
    def update(self):
        pygame.event.get()
        
        for i in range(len(self.joysticks)):
            joystick = self.joysticks[i]
            ui_joystick = self.ui.joysticks[i]
            
            ui_axes = ui_joystick[0]
            is_xbox = joystick.get_numaxes() == 5
            for axis in range(joystick.get_numaxes()):
                if is_xbox:
                    if axis <= 1:
                        #Left X/Y - These two are fine
                        ui_current_axis = ui_axes[axis]
                        value = joystick.get_axis(axis)
                        ui_current_axis.set_value(value)
                    elif axis == 2:
                        #Triggers - Left needs to be on axis 2, right needs to be on axis 3
                        ui_left_trigger = ui_axes[2]
                        ui_right_trigger = ui_axes[3]
                        value = joystick.get_axis(2)

                        if value > 0:
                            ui_left_trigger.set_value(value);
                            ui_right_trigger.set_value(0);
                        else:
                            ui_left_trigger.set_value(0);
                            ui_right_trigger.set_value(-value);
                            
                    elif axis == 3:
                        #Right Y- This is supposed to be on axis 5
                        ui_current_axis = ui_axes[5]
                        
                        value = joystick.get_axis(3)
                        ui_current_axis.set_value(value)
                    elif axis == 4:
                        #Right X= this is fine
                        ui_current_axis = ui_axes[axis]
                        value = joystick.get_axis(axis)
                        ui_current_axis.set_value(value)
                        
                else:
                    ui_current_axis = ui_axes[axis]
                    
                    value = joystick.get_axis(axis)
                    ui_current_axis.set_value(value)
                
            ui_buttons = ui_joystick[1]
            for button in range(joystick.get_numbuttons()):
                if button == 10:
                    break
                
                ui_current_button = ui_buttons[button]
                ui_current_button = ui_current_button[0]
                
                value = joystick.get_button(button)
                
                if value == False:
                    ui_current_button.deselect()
                else:
                    ui_current_button.select()
