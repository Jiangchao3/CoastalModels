'''
Arc StormSurge
Integrating Hurricane Storm Surge Modeling and GIS
 
--------------------------
Citation:
Ferreira, Celso M., Francisco Olivera, and Jennifer L. Irish, 2014. Arc StormSurge: Integrating Hurricane Storm Surge Modeling and GIS. Journal of the American Water Resources Association (JAWRA) 50(1): 219-233. DOI: 10.1111/jawr.12127
 
***********************************
 
Module: SWAN+ADCIRC PRE-PROCESSING
 
Title:  wave_refraction_in_swan
 
Description: Populates the fields  <nodeID> and <value> (wave_refraction_in_swan)
 
-------------------------
 
Script Instructions: Replace the path for the file location of the input and output files
 
-------------------------
Input files:
fort.13
 
Output files:
WaveRefrac.dbf
 
***********************************
Version history: 
Version 4
Author: Eric Ong
Created on January 23, 2015
Comments: Creation, development and testing for ArcGIS 10.2  

Future Improvements: Implement into ArcTool Box 
***********************************
'''

# Import modules

import time
import arcpy
import os
arcpy.env.overwriteOutput = True
print("Start working...")
startTime = time.clock()

try:
    def makeTable():
        txtFile = arcpy.GetParameterAsText(0)
        newTB = arcpy.GetParameterAsText(1)

        arcpy.CreateTable_management(os.path.dirname(newTB), os.path.basename(newTB),)


        #Add attribute fields to table
        arcpy.AddField_management(newTB,"NodeID","long")
        arcpy.AddField_management(newTB,"WaveRefrac","float")

        #Open the text file and read the number of nodes
        input = file(txtFile, "r")
        input.readline()
        line = input.readline()
        totalNodes=line.split() #Number of nodes
        nunnodes = int(totalNodes[0])
        line = input.readline()
        data=line.split()
        nunparameter=int(data[0]) #Number of attributes

        print('This ADCIRC GRID has: ' + str(nunnodes) + ' nodes')
        print('This Fort.13 file has: ' + str(nunparameter) + ' parameters')
        print('Importing the parameters from the Fort.13 ...')

        #Reads line until line with parameter
        count=0
        while count == 0:
            line = input.readline()
            data = line.split()
            if str(data[0]) == str("wave_refraction_in_swan"):
                count=+1

        line = input.readline()
        line = input.readline()
        line = input.readline()
        data = line.split()
        surfaceHeight = float(data[0])

        cur = arcpy.InsertCursor(newTB)
        index=1
        for row in range (0,nunnodes):
            row = cur.newRow()
            row.NodeID = long(index)
            row.WaveRefrac = surfaceHeight
            cur.insertRow(row)
            index=index+1       
        del cur, row

        #Adds non-default values
        count2=0
        while count2 == 0:
            line = input.readline()
            data = line.split()
            if str(data[0]) == str('wave_refraction_in_swan'):
                count2=+1
                
        line = input.readline()
        totalValues = line.split()

        if int(line) > 0:
            cur2 = arcpy.UpdateCursor(newTB)
            for i in range(int(line)):
                line=input.readline()
                data=line.split()
                tmpnode = long(data[0])
                row = cur2.next()
                tmpnode2 = row.NodeID
                while tmpnode <> tmpnode2:
                    row = cur2.next()
                    tmpnode2 = row.NodeID
                row.WaveRefrac = float(data[1])
                cur2.updateRow(row)
            del row, cur2
            line = input.readline()

        arcpy.DeleteField_management(newTB, "Field1")
        input.close()
    makeTable()

    print("End of Script, Process Completed Successfully!")
    stopTime = time.clock()
    elapTime = stopTime - startTime
    print("Total time to run the script: " + str(round(elapTime)) + " seconds")

except:
    arcpy.AddMessage("Error while running script...")
