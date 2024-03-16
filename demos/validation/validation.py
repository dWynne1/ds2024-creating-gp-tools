class ToolValidator:
    """Class to add custom behavior and properties to the tool and tool parameters."""

    def __init__(self):
        """Set self.params for use in other functions"""
        self.params = arcpy.GetParameterInfo()

    def initializeParameters(self):
        """Customize parameter properties. 
        This gets called when the tool is opened."""
        
        return

    def updateParameters(self):
        """Modify parameter values and properties.
        This gets called each time a parameter is modified, before 
        standard validation."""

        if self.params[3].valueAsText == 'POINT':
            self.params[4].enabled = False  # Turn Feature Set OFF
            self.params[4].value = None     
        
            self.params[5].enabled = True   # Turn Point ON
            
            # For demo purposes, I'm setting the coordinates, so that I don't have 
            # to type them in.        
            self.params[5].value = "-13014050.8258 4040432.7741"

        else:
            self.params[4].enabled = True   # Turn Feature Set ON
            
            self.params[5].enabled = False  # Turn Point OFF
            self.params[5].value = None
            
        return

    def updateMessages(self):
        """Customize messages for the parameters.
        This gets called after standard validation."""
       
        # Use Error 530 when logic dictates that an optional parameter needs a value

        if self.params[3].valueAsText == 'POINT':
            if not self.params[5].valueAsText:
                self.params[5].setIDMessage('ERROR', 530)
        else:
            if not self.params[4].valueAsText:
                self.params[4].setIDMessage('ERROR', 530)
        
        return

    def isLicensed(self):
        """An optional method to set whether a tool is licensed."""
        
        return True
        
    def postExecute(self):
        """An optional method to update the display when the tool is finished"""
        
        return