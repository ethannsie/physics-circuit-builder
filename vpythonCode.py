Web VPython 3.2
scene = canvas(width=1250, height=400)
#scene.camera.pos = vector(0, 10, 0)
#scene.camera.axis = vector(0, -1, 0)
scene.userspin = False
scene.camera.pos = vec(-0.486395, 610.798, 3.87329e-4)
scene.camera.axis = vec(0.486395, -610.798, -3.87329e-4)

img_url = "https://i.imgur.com/2EUXcR2.jpeg"
img_url = "https://i.imgur.com/EIx2SYP.jpeg"
img_url = "https://i.imgur.com/d0Ttm7l.jpeg"
# used to regulate buttons that may overwrite each other

is_running = False
circuitBuild = True
specialMode = False
allCircuitLoops = []

junctionList = []
allJunctions = []
junctionHighlight = []

wireHighlight = [] 
wireHighlightLabels = []
allWires = []
actualAllWires = []

wireCounter = 1

wireLabels = []
initial_circuit = []
arrows = []
gridLength = 1
dimension = 10
sideLength = 20


#circuitBuild = text(text='Circuit Building Enabled', pos = vector(3*sideLength, 0, 0), align='center', color=color.green, billboard = True, height=sideLength/2)
#junctionShow = text(text='Show Junctions Enabled', pos = vector(2*sideLength, 0, 0), align='center', color=color.green, billboard = True, height=sideLength/2)
#kvlShow = text(text='Show KVL Enabled', pos = vector(1*sideLength, 0, 0), align='center', color=color.green, billboard = True, height=sideLength/2)
#currentShow = text(text='Show Currents Enabled', pos = vector(0*sideLength, 0, 0), align='center', color=color.green, billboard = True, height=sideLength/2)
#sharafShow = text(text='Show Sharaf Enabled', pos = vector(-1*sideLength, 0, 0), align='center', color=color.green, billboard = True, height=sideLength/2)

highlightBoxes = []
kvlLoops = []

allResistors = []
allEMF = []

# sets up an axis for testing
# x is up down
# z is right left
#box(canvas = scene, pos=vector(0, 0, 0), length=gridLength, width=gridLength, height=gridLength, color=color.yellow)
#for i in range(100):
#    box(canvas = scene, pos=vector(gridLength*(i+1), 0, 0), length=gridLength, width=gridLength, height=gridLength, color=color.red)
#for i in range(100):
#    box(canvas = scene, pos=vector(0, gridLength*(i+1), 0), length=gridLength, width=gridLength, height=gridLength, color=color.green)
#for i in range(100):
#    box(canvas = scene, pos=vector(0, 0, gridLength*(i+1)), length=gridLength, width=gridLength, height=gridLength, color=color.blue)

def euler():
    n = 10000000
    e = (1+1/n)**n
    return e

def draw_resistor(wire, orientation):
    center = wire.pos
    l = wire.length * 0.6
    h = wire.height * 0.2
    
    if orientation == 'x':
        for i in range(5):
            start = vector(center.x - l/2 + i*l/4, center.y + wire.height/2 + h, center.z)
            end = vector(center.x - l/2 + (i+1)*l/4, center.y + wire.height/2 + (h if i%2==1 else -h), center.z)
            resistor = cylinder(canvas = scene, pos=start, axis=end-start, radius=wire.width*0.075, color=color.orange)
            resistor.center = center
            allResistors.append(resistor)
    elif orientation == 'z':
        for i in range(5):
            start = vector(center.x, center.y + wire.height/2 + h, center.z - l/2 + i*l/4)
            end = vector(center.x, center.y + wire.height/2 + (h if i%2==1 else -h), center.z - l/2 + (i+1)*l/4)
            resistor = cylinder(canvas = scene, pos=start, axis=end-start, radius=wire.width*0.075, color=color.orange)
            resistor.center = center
            allResistors.append(resistor)

def draw_emf(block, emfDirection, orientation):
    center = block.pos
    offset = block.length * 0.15
    if orientation == 'x':
        if emfDirection == "posToNeg":
            # pos terminal (longer line)
            emf1 = cylinder(canvas = scene, pos=vector(center.x - offset, center.y + block.height/2 + 1, center.z),
                              axis=vector(0.15 * block.length, 0, 0), radius=block.width * 0.1, color=color.red)
            emf1.center = center
            # neg terminal (shorter line)
            emf2 = cylinder(canvas = scene, pos=vector(center.x + offset, center.y + block.height/2 + 1, center.z),
                              axis=vector(0.05 * block.length, 0, 0), radius=block.width * 0.1, color=color.black)
            allEMF.append([emf1,emf2])
        else:
            emf1 = cylinder(canvas = scene, pos=vector(center.x + offset, center.y + block.height/2 + 1, center.z),
                              axis=vector(0.15 * block.length, 0, 0), radius=block.width * 0.1, color=color.red)
            emf1.center = center
            
            emf2 = cylinder(canvas = scene, pos=vector(center.x - offset, center.y + block.height/2 + 1, center.z),
                              axis=vector(0.05 * block.length, 0, 0), radius=block.width * 0.1, color=color.black)
            allEMF.append([emf1, emf2])
    elif orientation == 'z':
        if emfDirection == "posToNeg":
            emf1 = cylinder(canvas=scene, pos=vector(center.x, center.y + block.height/2 + 1, center.z - offset),
                                  axis=vector(0, 0, 0.15 * block.length), radius=block.width * 0.1, color=color.red)
            emf1.center = center
            emf2 = cylinder(canvas=scene,pos=vector(center.x, center.y + block.height/2 + 1, center.z + offset),
                                  axis=vector(0, 0, 0.05 * block.length), radius=block.width * 0.1, color=color.black)
            allEMF.append([emf1, emf2])
        else:
            emf1 = cylinder(canvas=scene,pos=vector(center.x, center.y + block.height/2 + 1, center.z + offset),
                                  axis=vector(0, 0, 0.15 * block.length), radius=block.width * 0.1, color=color.red)
            emf2 = cylinder(canvas=scene,pos=vector(center.x, center.y + block.height/2 + 1, center.z - offset),
                                  axis=vector(0, 0, 0.05 * block.length), radius=block.width * 0.1, color=color.black)
            emf1.center = center
            allEMF.append([emf1, emf2])

def draw_wire(wire, orientation='x'):
    center = wire.pos
    offset = wire.height/2 + 1
    length = wire.length * 0.8 
    radius = wire.width * 0.05  
    #down/up
    if orientation == 'x':
        axis = vector(length, 0, 0)
        pos = vector(center.x - length/2, center.y + offset, center.z)
    #left/right
    elif orientation == 'z':
        axis = vector(0, 0, length)
        pos = vector(center.x, center.y + offset, center.z - length/2)

    word = cylinder(canvas=scene,pos=pos, axis=axis, radius=radius, color=color.gray(0.5))
    word.center = center
    allWires.append(word)
    
def create_initial_circuit():
    global is_running
    global junctionList
    global kvlLoops
    global junctionHighlight
    global wireHighlight
    global allWires
    global actualAllWires
    global wireCounter
    
    if is_running or len(junctionList) > 0:
        return
    is_running = True
    try:
        global initial_circuit
        global dimension
        global sideLength
        global allCircuitLoops
        
        directionToVector = {"x":vec(1, 0, 0), "-x":vec(-1,0,0), "z":vec(0, 0, 1), "-z":vec(0, 0, -1)}
        
        wire = box(canvas=scene, pos=vector(-(dimension-1)/2*sideLength, 0, -(dimension-1)/2*sideLength), length=sideLength, width=sideLength, height=sideLength, color=vector(0.45, 0.8, 0.75))
        wire.element = "Junction Wire"
        wire.extend = "LEFT"
        junctionList.append(wire)
        allJunctions.append(wire)
        
        highlight = box(canvas=scene,pos=wire.pos, length=sideLength*1.25, width=sideLength*1.25, height=sideLength*1.25, color=vector(0.4, 0.7, 1), opacity=0.6)
        highlight.visible = False
        junctionHighlight.append(highlight)
        
        wire.directionIn = ["-z"]
        wire.directionOut = ["x"]
        initial_circuit.append(wire)
        
        totalWire = []
        
        for i in range(dimension-2):
            wire = box(canvas=scene,pos=vector(-(dimension-1)/2*sideLength + sideLength*(i+1), 0, -(dimension-1)/2*sideLength), length=sideLength, width=sideLength, height=sideLength, color=color.white)
            if i == 0:
                wire.element = "Resistor"
                wire.resistance = 2
                draw_resistor(wire, 'x')
            if i == 1:
                wire.element = "EMF"
                wire.flow = "posToNeg"
                wire.voltage = 10
                draw_emf(wire, "posToNeg", 'x')
            if i > 1:
                wire.element = "Wire"
                draw_wire(wire)
            wire.directionIn = ["x"]
            wire.directionOut = ["x"]
            wire.wir = wireCounter
            initial_circuit.append(wire)
            if i == 0:
                arro = arrow(canvas=scene,shaftwidth=sideLength/3,pos=vector(wire.pos.x, wire.pos.y, wire.pos.z+sideLength), axis=(dimension-3)*sideLength*directionToVector[wire.directionIn[0]], color=vector(0.21, 0.82, 0.85))
                arro.visible = False
                kvlLoops.append(arro)
            totalWire.append(wire)
            
            highlight = box(canvas=scene, pos=wire.pos, length=sideLength*1.125, width=sideLength*1.125,height=sideLength*1.125, color=vector(0.8, 0.65, 1), opacity=0.6)
            highlight.visible = False
            wireHighlight.append(highlight)
        
        wireCounter += 1   
        actualAllWires.append(totalWire)
        allWires.append(totalWire)
    
        wire = box(canvas=scene,pos=vector(-(dimension-1)/2*sideLength + sideLength*(dimension-1), 0, -(dimension-1)/2*sideLength), length=sideLength, width=sideLength, height=sideLength, color=vector(0.45, 0.8, 0.75))
        wire.element = "Junction Wire"
        wire.extend = "UP"
        highlight = box(canvas=scene,pos=wire.pos, length=sideLength*1.25, width=sideLength*1.25, height=sideLength*1.25, color=vector(0.4, 0.7, 1), opacity=0.6)
        highlight.visible = False
        junctionHighlight.append(highlight)
        junctionList.append(wire)
        allJunctions.append(wire)
        wire.directionIn = ["x"]
        wire.directionOut = ["z"]
        initial_circuit.append(wire)
        
        totalWire = []
        for i in range(dimension-2):
            wire = box(canvas=scene,pos=vector(-(dimension-1)/2*sideLength + sideLength*(dimension-1), 0, -(dimension-1)/2*sideLength + (i+1)*sideLength), length=sideLength, width=sideLength, height=sideLength, color=color.white)
            if i == 0:
                wire.element = "Resistor"
                wire.resistance = 2
                draw_resistor(wire, 'z')
            if i > 0:
                wire.element = "Wire"
                draw_wire(wire, "z")
            wire.directionIn = ["z"]
            wire.directionOut = ["z"]
            wire.wir = wireCounter
            initial_circuit.append(wire)
            if i == 0:
                arro = arrow(canvas=scene,shaftwidth=sideLength/3,pos=vector(wire.pos.x-sideLength, wire.pos.y, wire.pos.z), axis=(dimension-3)*sideLength*directionToVector[wire.directionIn[0]], color=vector(0.21, 0.82, 0.85))
                arro.visible = False
                kvlLoops.append(arro)
            
            highlight = box(canvas=scene,pos=wire.pos, length=sideLength*1.125, width=sideLength*1.125, height=sideLength*1.125, color=vector(0.8, 0.65, 1), opacity=0.6)
            highlight.visible = False
            wireHighlight.append(highlight)
            
            totalWire.append(wire)
        
        wireCounter += 1   
        allWires.append(totalWire) 
        actualAllWires.append(totalWire)
        
        wire = box(canvas=scene,pos=vector(-(dimension-1)/2*sideLength + sideLength*(dimension-1), 0, -(dimension-1)/2*sideLength + (dimension-1)*sideLength), length=sideLength, width=sideLength, height=sideLength, color=vector(0.45, 0.8, 0.75))
        wire.element = "Junction Wire"
        wire.extend = "RIGHT"
        junctionList.append(wire)
        highlight = box(canvas=scene,pos=wire.pos, length=sideLength*1.25, width=sideLength*1.25, height=sideLength*1.25, color=vector(0.4, 0.7, 1), opacity=0.6)
        highlight.visible = False
        junctionHighlight.append(highlight)
        allJunctions.append(wire)
        wire.directionIn = ["z"]
        wire.directionOut = ["-x"]
        initial_circuit.append(wire)
        
        totalWire = []
        for i in range(dimension-2):
            wire = box(canvas=scene,pos=vector(-(dimension-1)/2*sideLength + sideLength*(dimension-1)-sideLength*(i+1), 0, -(dimension-1)/2*sideLength + (dimension-1)*sideLength), length=sideLength, width=sideLength, height=sideLength, color=color.white)
            if i == 0:
                wire.element = "Resistor"
                wire.resistance = 2
                draw_resistor(wire, 'x')
            if i > 0:
                wire.element = "Wire"
                draw_wire(wire)
            wire.directionIn = ["-x"]
            wire.directionOut = ["-x"]
            wire.wir = wireCounter
            initial_circuit.append(wire)
            if i == 0:
                arro = arrow(canvas=scene,shaftwidth=sideLength/3,pos=vector(wire.pos.x, wire.pos.y, wire.pos.z-sideLength), axis=(dimension-3)*sideLength*directionToVector[wire.directionIn[0]], color=vector(0.21, 0.82, 0.85))
                arro.visible = False
                kvlLoops.append(arro)
            
            highlight = box(canvas=scene,pos=wire.pos, length=sideLength*1.125, width=sideLength*1.125, height=sideLength*1.125, color=vector(0.8, 0.65, 1), opacity=0.6)
            highlight.visible = False
            wireHighlight.append(highlight)
            
            totalWire.append(wire)
            
        wireCounter += 1    
        allWires.append(totalWire)
        actualAllWires.append(totalWire)
        
        wire = box(canvas=scene,pos=vector(-(dimension-1)/2*sideLength + sideLength*(dimension-1)-sideLength*(dimension-1), 0, -(dimension-1)/2*sideLength + (dimension-1)*sideLength), length=sideLength, width=sideLength, height=sideLength, color=vector(0.45, 0.8, 0.75))
        wire.element = "Junction Wire"
        wire.extend = "DOWN"
        junctionList.append(wire)
        allJunctions.append(wire)
        highlight = box(canvas=scene,pos=wire.pos, length=sideLength*1.25, width=sideLength*1.25, height=sideLength*1.25, color=vector(0.4, 0.7, 1), opacity=0.6)
        highlight.visible = False
        junctionHighlight.append(highlight)
        wire.directionIn = ["-x"]
        wire.directionOut = ["-z"]
        initial_circuit.append(wire)
        
        totalWire = []
        for i in range(dimension-2):
            wire = box(canvas=scene,pos=vector(-(dimension-1)/2*sideLength + sideLength*(dimension-1)-sideLength*(dimension-1), 0, -(dimension-1)/2*sideLength + (dimension-1)*sideLength - (i+1)*sideLength), length=sideLength, width=sideLength, height=sideLength, color=color.white)
            if i == 0:
                wire.element = "Resistor"
                wire.resistance = 2
                draw_resistor(wire, 'z')
            if i > 0:
                wire.element = "Wire"
                draw_wire(wire, "z")
            wire.directionIn = ["-z"]
            wire.directionOut = ["-z"]
            wire.wir = wireCounter
            initial_circuit.append(wire)
            if i == 0:
                arro = arrow(canvas=scene,shaftwidth=sideLength/3,pos=vector(wire.pos.x+sideLength, wire.pos.y, wire.pos.z), axis=(dimension-3)*sideLength*directionToVector[wire.directionIn[0]], color=vector(0.21, 0.82, 0.85))
                arro.visible = False
                kvlLoops.append(arro)
            highlight = box(canvas=scene,pos=wire.pos, length=sideLength*1.125, width=sideLength*1.125, height=sideLength*1.125, color=vector(0.8, 0.65, 1), opacity=0.6)
            highlight.visible = False
            wireHighlight.append(highlight)
            
            totalWire.append(wire)
        wireCounter += 1    
        allWires.append(totalWire)
        actualAllWires.append(totalWire)
        
        
        allCircuitLoops.append(initial_circuit)
#        print(checkBlockExists(vector(0, 0, 0)))
        drawExtensionArrows()
    finally:
        is_running = False

def add_block_segment(start_pos, direction, dimension, sideLength, label_color=color.green):
    blocks = []
    global kvlLoops
    global wireHighlight
    global totalWire
    global allCircuitLoops
    global wireCounter
    
    direction_vector = {
        'UP': vector(1, 0, 0),
        'DOWN': vector(-1, 0, 0),
        'LEFT': vector(0, 0, -1),
        'RIGHT': vector(0, 0, 1)
    }[direction]
    
    directionToVector = {"x":vec(1, 0, 0), "-x":vec(-1,0,0), "z":vec(0, 0, 1), "-z":vec(0, 0, -1)}
    
    totalWire = []
    for i in range(dimension-2):
        pos = start_pos + i * sideLength * direction_vector
        block = box(canvas=scene,pos=pos, length=sideLength, width=sideLength, height=sideLength, color=color.white)
        highlight = box(canvas=scene,pos=block.pos, length=sideLength*1.125, width=sideLength*1.125, height=sideLength*1.125, color=vector(0.8, 0.65, 1), opacity=0.6)
        highlight.visible = False
        wireHighlight.append(highlight)
        block.wir = wireCounter
        totalWire.append(block)
            
        if i == 0:
            block.element = "Resistor"
            block.resistance = 2
            if direction == "UP" or direction == "DOWN":
                draw_resistor(block, 'x')
                if direction == "UP":
                    block.directionIn = ["x"]
                    block.directionOut = ["x"]
                    arro = arrow(canvas=scene,shaftwidth=sideLength/3,pos=vector(block.pos.x, block.pos.y, block.pos.z+sideLength), axis=(dimension-3)*sideLength*directionToVector[block.directionIn[0]], color=vector(0.21, 0.82, 0.85))
                    arro.visible = False
                    kvlLoops.append(arro)
                else:
                    block.directionIn = ["-x"]
                    block.directionOut = ["-x"]
                    arro = arrow(canvas=scene,shaftwidth=sideLength/3,pos=vector(block.pos.x, block.pos.y, block.pos.z-sideLength), axis=(dimension-3)*sideLength*directionToVector[block.directionIn[0]], color=vector(0.21, 0.82, 0.85))
                    arro.visible = False
                    kvlLoops.append(arro)
            elif direction == "RIGHT" or direction == "LEFT":
                draw_resistor(block, 'z')
                if direction == "RIGHT":
                    block.directionIn = ["z"]
                    block.directionOut = ["z"]
                    arro = arrow(canvas=scene,shaftwidth=sideLength/3,pos=vector(block.pos.x-sideLength, block.pos.y, block.pos.z), axis=(dimension-3)*sideLength*directionToVector[block.directionIn[0]], color=vector(0.21, 0.82, 0.85))
                    arro.visible = False
                    kvlLoops.append(arro)
                else:
                    block.directionIn = ["-z"]
                    block.directionOut = ["-z"]
                    arro = arrow(canvas=scene,shaftwidth=sideLength/3,pos=vector(block.pos.x+sideLength, block.pos.y, block.pos.z), axis=(dimension-3)*sideLength*directionToVector[block.directionIn[0]], color=vector(0.21, 0.82, 0.85))
                    arro.visible = False
                    kvlLoops.append(arro)
        else:
            block.element = "Wire"
            if direction == "UP" or direction == "DOWN":
                draw_wire(block, 'x')
                if direction == "UP":
                    block.directionIn = ["x"]
                    block.directionOut = ["x"]
                else:
                    block.directionIn = ["-x"]
                    block.directionOut = ["-x"]
            elif direction == "RIGHT" or direction == "LEFT":
                draw_wire(block, 'z')
                if direction == "RIGHT":
                    block.directionIn = ["z"]
                    block.directionOut = ["z"]
                else:
                    block.directionIn = ["-z"]
                    block.directionOut = ["-z"]

#        block.directionIn = [opposite_direction(direction)]
#        block.directionOut = [direction]
        
        blocks.append(block)
    wireCounter += 1
    allWires.append(totalWire)
    actualAllWires.append(totalWire)
    
    return blocks


def checkBlockExists(check_pos):
    global allCircuitLoops

    for loop in allCircuitLoops:
        for block in loop:
            if block.pos == check_pos:
                return True
    return False

def checkWireBlockExists(check_pos):
    global actualAllWires
    
    for wire in actualAllWires:
        for block in wire:
            if block.pos == check_pos:
                return True
    return False
    
def extend_circuit(direction, initial_pos):   
    if circuitBuild:
        global dimension
        global sideLength
        global junctionList
        global allCircuitLoops
        global arrows
            
        directList = ["UP", "RIGHT", "DOWN", "LEFT"]
        
        firstBlock_pos = vector(initial_pos.pos.x, initial_pos.pos.y, initial_pos.pos.z)
        
        if direction == "UP":
            firstBlock_pos = firstBlock_pos + vector(sideLength, 0, 0)
        elif direction == "DOWN":
            firstBlock_pos = firstBlock_pos + vector(-sideLength, 0, 0)
        elif direction == "LEFT":
            firstBlock_pos = firstBlock_pos + vector(0, 0, -sideLength)
        elif direction == "RIGHT":
            firstBlock_pos = firstBlock_pos + vector(0, 0, sideLength)
        
        loop = []
        currentDirection = direction
        
     #   max_iterations = 100
     #   iterations = 0
        
        while checkBlockExists(firstBlock_pos) == False and findClosestBlock(initial_pos.pos) in allJunctions:
    #        if iterations > max_iterations:
    #            print("Reached max iterations, breaking to avoid infinite loop.")
    #            break
            
            # Add segment blocks in current direction
            blocks = add_block_segment(firstBlock_pos, currentDirection, dimension, sideLength)
            
            loop.extend(blocks)
            
            lastBlockPos = blocks[-1].pos
            
            # Calculate next junction position based on currentDirection and last block
            if currentDirection == "UP":
                juncPos = lastBlockPos + vector(sideLength, 0, 0)
            elif currentDirection == "DOWN":
                juncPos = lastBlockPos + vector(-sideLength, 0, 0)
            elif currentDirection == "LEFT":
                juncPos = lastBlockPos + vector(0, 0, -sideLength)
            elif currentDirection == "RIGHT":
                juncPos = lastBlockPos + vector(0, 0, sideLength)
            
            # Only add junction block if it does not exist yet
            if checkBlockExists(juncPos) == False:
                block = box(canvas=scene,pos=juncPos, length=sideLength, width=sideLength, height=sideLength, color=vector(0.45, 0.8, 0.75))
                block.extend = currentDirection
                allJunctions.append(block)
                
                highlight = box(canvas=scene,pos=block.pos, length=sideLength*1.25, width=sideLength*1.25, height=sideLength*1.25, color=vector(0.4, 0.7, 1), opacity=0.6)
                highlight.visible = False
                junctionHighlight.append(highlight)
                
#                print(allJunctions)
                if currentDirection == direction:
                    junctionList.append(block)
                loop.append(block)
            else:
                block = blockAtPos(juncPos) 
    #            block.extend = "None"
    #            for arrow in arrows:
    #                arrow.visible = False
            
    #        if block.extend != direction and block not in junctionList:
    #            block.extend = "None"
                
            # Move direction to next in directList
            currentIndex = directList.index(currentDirection)
            currentDirection = directList[(currentIndex + 1) % 4]
            
            # Update firstBlock_pos for the next iteration based on the new junction position and direction
            if currentDirection == "UP":
                firstBlock_pos = juncPos + vector(sideLength, 0, 0)
            elif currentDirection == "DOWN":
                firstBlock_pos = juncPos + vector(-sideLength, 0, 0)
            elif currentDirection == "LEFT":
                firstBlock_pos = juncPos + vector(0, 0, -sideLength)
            elif currentDirection == "RIGHT":
                firstBlock_pos = juncPos + vector(0, 0, sideLength)
            
     #       iterations += 1
        
        allCircuitLoops.append(loop)
        drawExtensionArrows()
        
    #    for direct in directions:
    #        for arrow in arrows:
    #            if direct == arrow.direction:
    #                arrow.visible = False
        if len(junctionHighlight) > 0 and junctionHighlight[0].visible:
            showJunc()
            
        if len(kvlLoops) > 0 and kvlLoops[0].visible:
            showKVL()
            
        if len(wireHighlight) > 0 and wireHighlight[0].visible:
            showWires()
        
        if specialMode:
            specialModeEnable()
            
def blockAtPos(position):
    global allCircuitLoops
    for loop in allCircuitLoops:
        for block in loop:
            if block.pos == position:
                return block
    return "NO"
scene.bind("click", handle_click)

def euclideanDistance(pos_1, pos_2):
    return ((pos_1.x - pos_2.x)**2 + (pos_1.y - pos_2.y)**2 + (pos_1.z - pos_2.z)**2)**0.5

def findClosestJunc(current_pos):
    global junctionList
    origin = vector(0, 0, 0)
    closestBlock = box(canvas=scene)
    closestBlock.visible = False
    minDist = 10000000000000000
    for junction in junctionList:
        distance = euclideanDistance(junction.pos, current_pos)
        if distance < minDist:
            closestBlock = junction
            minDist = distance
    return closestBlock
    
def junkCode(current_pos):
    global allJunctions
    origin = vector(0, 0, 0)
    closestBlock = box(canvas=scene)
    closestBlock.visible = False
    minDist = 10000000000000000
    for junction in allJunctions:
        distance = euclideanDistance(junction.pos, current_pos)
        if distance < minDist:
            closestBlock = junction
            minDist = distance
    return closestBlock

def findClosestBlock(current_pos):
    global allCircuitLoops
    origin = vector(0, 0, 0)
    closestBlock = box(canvas=scene)
    closestBlock.visible = False
    minDist = 10000000000000000
    for loop in allCircuitLoops:
        for block in loop:
            distance = euclideanDistance(block.pos, current_pos)
            if distance < minDist:
                closestBlock = block
                minDist = distance
    return closestBlock
    
def drawExtensionArrows():
    global junctionList
    global sideLength
    global arrows
    directions = []
    for junction in junctionList:
        ax = vec(0, 0, 0)
        if junction.extend == "UP":
            ax = vec(sideLength * 2, 0, 0)
        elif junction.extend == "DOWN":
            ax = vec(-1 * sideLength * 2, 0, 0)
        elif junction.extend == "RIGHT":
            ax = vec(0, 0, sideLength * 2)
        elif junction.extend == "LEFT":
            ax = vec(0, 0, -1 * sideLength * 2)
        obj = arrow(canvas=scene,pos=junction.pos, axis=ax, color=vector(0.21, 0.82, 0.85))
        directions.append(junction.extend)
        arrow.direction = junction.extend
        arrows.append(obj)
        
def handle_click(event):
    global allCircuitLoops
    global sideLength
    global highlightBoxes
    global circuitBuild
    global wireHighlightLabels
    global extractedCurrents
    global is_running
    
    matrix = kclCalculate()
    
    kvlLoops = kvlCalculate()
    for loop in kvlLoops:
        matrix.append(loop)
    
    currents = rref(matrix)

    extractedCurrents = []
    
    for i in range(len(actualAllWires)):
        extractedCurrents.append(currents[i][len(actualAllWires)])
        
    if is_running:
    #    print("Busy! Wait for the current operation to finish.")
        return
    
    is_running = True
    try:
        click_pos = event.pos
        testVector = vector(click_pos.x, 0, click_pos.z)
        block = findClosestJunc(testVector)
    #    print(block.pos)
    #    print(block.extend)
        extend_circuit(block.extend, block)
    #    print("Clicked at:", testVector)
    #    print(allCircuitLoops)
        if circuitBuild == False and len(allCircuitLoops) > 0:
            block = findClosestBlock(testVector)
            if findClosestBlock(testVector) != junkCode(testVector):
                highlight = box(canvas=scene,pos=block.pos, length=sideLength*1.25, width=sideLength*1.25, height=sideLength*1.25, color=color.cyan, opacity=0.6)
                highlightBoxes.append(highlight)
                
                if block.element == "EMF":
                    highlightLabel = label(
                    canvas=scene,
                    pos=block.pos + vector(0, sideLength*1.5, 0), 
                    text=f"Circuit Element: {block.element} \n Wire: {block.wir} \n Current: {round(extractedCurrents[block.wir-1], 2)} A \n Voltage: {block.voltage} V\n Resistance: 0 Ω",
                    xoffset=25, yoffset=0, space=30,
                    height=16, border=2, font='sans'
                    )
                elif block.element == "Resistor":
                    highlightLabel = label(
                    canvas=scene,
                    pos=block.pos + vector(0, sideLength*1.5, 0), 
                    text=f"Circuit Element: {block.element} \n Wire: {block.wir} \n Current: {round(extractedCurrents[block.wir-1], 2)} A \n Voltage: {round(block.resistance * extractedCurrents[block.wir-1], 2)} V\n Resistance: {block.resistance} Ω",
                    xoffset=25, yoffset=0, space=30,
                    height=16, border=2, font='sans'
                    )
                elif block.element == "Wire":
                    highlightLabel = label(
                    canvas=scene,
                    pos=block.pos + vector(0, sideLength*1.5, 0), 
                    text=f"Circuit Element: {block.element} \n Wire: {block.wir} \n Current: {round(extractedCurrents[block.wir-1], 2)} A",
                    xoffset=25, yoffset=0, space=30,
                    height=16, border=2, font='sans'
                    )
                wireHighlightLabels.append(highlightLabel)
                
                if block.element == "EMF":
                    my_slider.value = abs(block.voltage)
                    val_text.text = f"Current Value: {block.voltage:.2f} V\n"
                elif block.element == "Resistor":
                    my_slider.value = block.resistance
                    val_text.text = f"Current Value: {block.resistance:.2f} Ω\n"
                elif block.element == "Wire":
                    my_slider.value = 0
                    val_text.text = "Not Adjustable\n"
                    
            if len(highlightBoxes) > 1:
                highlightBoxes[len(highlightBoxes)-2].visible = False
                wireHighlightLabels[len(wireHighlightLabels)-2].visible = False
        else:
            if len(highlightBoxes) > 1:
                highlightBoxes[len(highlightBoxes)-1].visible = False
                wireHighlightLabels[len(wireHighlightLabels)-1].visible = False
    finally:
        is_running = False
        

def adjustElementValue(s):
    global highlightBoxes
    global wireHighlight

    if not highlightBoxes:
        return

    elem = findClosestBlock(highlightBoxes[-1].pos)
    if elem.element == "EMF":
        if elem.flow == "posToNeg":
            elem.voltage = s.value
        else:
            elem.voltage = -1 * s.value
        val_text.text = f"Current Value: {elem.voltage} V\n"
    elif elem.element == "Resistor":
        elem.resistance = s.value
        val_text.text = f"Current Value: {s.value:.2f} Ω\n"
    elif elem.element == "Wire":
        val_text.text = "Not Adjustable\n"
    if wireHighlight and wireHighlight[0].visible:
        hideWires()
        showWires()

  
def is_adjacent_to_junction(block, junction, sideLength):
    dx = abs(block.pos.x - junction.pos.x)
    dz = abs(block.pos.z - junction.pos.z)
    dy = abs(block.pos.y - junction.pos.y)
    return (dy == 0) and (
        (dx == sideLength and dz == 0) or
        (dz == sideLength and dx == 0)
    )

def find_closing_wire_group(new_wire_groups, all_wire_groups, all_junctions, sideLength):
    first_new_block = new_wire_groups[0][0]
    last_new_block = new_wire_groups[-1][-1]
    start_junction = None
    end_junction = None
    for junction in all_junctions:
        if is_adjacent_to_junction(first_new_block, junction, sideLength):
            start_junction = junction
        if is_adjacent_to_junction(last_new_block, junction, sideLength):
            end_junction = junction
    if start_junction is None or end_junction is None:
        return None

    for group in all_wire_groups:
        if group in new_wire_groups:
            continue
        found_at_start = False
        found_at_end = False
        for block in group:
            if is_adjacent_to_junction(block, start_junction, sideLength):
                found_at_start = True
            if is_adjacent_to_junction(block, end_junction, sideLength):
                found_at_end = True
        if found_at_start and found_at_end:
            return group
    return None
    

def kvlCalculate():
    global actualAllWires
    global sideLength

    all_wire_groups = actualAllWires
    allKVL = []

    listSize = len(actualAllWires) + 1

    kvl = [0] * listSize
    kvlSum = 0

    for group in actualAllWires[:4]:
        for block in group:
            wireNum = getattr(block, "wir", None)
            if wireNum is None:
                continue
            wireNum = int(wireNum)
            # Use wireNum-1 for zero-based indexing
            if getattr(block, "element", "") == "Resistor":
                kvl[wireNum-1] += getattr(block, "resistance", 0)
            if getattr(block, "element", "") == "EMF":
                # Standard convention: subtract EMF in loop KVL
                kvlSum -= getattr(block, "voltage", 0)
    kvl[-1] = kvlSum
    allKVL.append(kvl)

    i = 4
    while i + 2 < len(actualAllWires):
        new_wire_groups = [actualAllWires[i], actualAllWires[i+1], actualAllWires[i+2]]
        closing_group = find_closing_wire_group(new_wire_groups, all_wire_groups, allJunctions, sideLength)
        if closing_group is None:
       #     print(f"Could not find closing wire group for KVL loop starting at {i}")
            i += 3
            continue
        kvl_loop = new_wire_groups + [closing_group]
        kvl = [0] * listSize
        kvlSum = 0
        for count, group in enumerate(kvl_loop):
            for block in group:
                wireNum = getattr(block, "wir", None)
                if wireNum is None:
                    continue
                wireNum = int(wireNum)
                if count != 3:
                    if getattr(block, "element", "") == "Resistor":
                        kvl[wireNum-1] += getattr(block, "resistance", 0)
                    if getattr(block, "element", "") == "EMF":
                        kvlSum += getattr(block, "voltage", 0)
                else:
                    if getattr(block, "element", "") == "Resistor":
                        kvl[wireNum-1] -= getattr(block, "resistance", 0)
                    if getattr(block, "element", "") == "EMF":
                        kvlSum += getattr(block, "voltage", 0)
        kvl[-1] = kvlSum
        allKVL.append(kvl)
        i += 3

    return allKVL
        
                    
def kclCalculate():
    global actualAllWires
    global dimension
    global allJunctions
    global sideLength
    
    allKCLS = []
    
#    directVect = {0:vec(1, 0, 0), 1:vec(0, 0, 1), 2:vec(-1, 0, 0), 3:vec(0, 0, -1)}
    listSize = len(actualAllWires) + 1
    
    for i in range(4):
        inWires = []
        outWires = []
        
        kcl = []
        
        for j in range(listSize):
            kcl.append(0)
        
        if i == 0:
            inWires.append(4)
            outWires.append(1)
            if blockAtPos(allJunctions[0].pos + vector(-1*sideLength,0,0)) != "NO":
               block = blockAtPos(allJunctions[0].pos + vector(-1*sideLength,0,0))
               inWires.append(block.wir)
            elif blockAtPos(allJunctions[0].pos + vector(0, 0, -1*sideLength)) != "NO":
                block = blockAtPos(allJunctions[0].pos + vector(0, 0, -1*sideLength))
                outWires.append(block.wir)
        elif i == 1:
            inWires.append(1)
            outWires.append(2)
            if blockAtPos(allJunctions[1].pos + vector(0, 0, -1*sideLength)) != "NO":
                block = blockAtPos(allJunctions[1].pos + vector(0, 0, -1*sideLength))
                inWires.append(block.wir)
            elif blockAtPos(allJunctions[1].pos + vector(sideLength,0,0)) != "NO":
                block = blockAtPos(allJunctions[1].pos + vector(sideLength,0,0))
                outWires.append(block.wir)
        elif i == 2:
            inWires.append(2)
            outWires.append(3)
            if blockAtPos(allJunctions[2].pos + vector(sideLength,0,0)) != "NO":
                block = blockAtPos(allJunctions[2].pos + vector(sideLength,0,0))
                inWires.append(block.wir)
            elif blockAtPos(allJunctions[2].pos + vector(0, 0, sideLength)) != "NO":
                block = blockAtPos(allJunctions[2].pos + vector(0, 0, sideLength))
                outWires.append(block.wir)
        elif i == 3:
            inWires.append(3)
            outWires.append(4)
            if blockAtPos(allJunctions[3].pos + vector(0, 0, sideLength)) != "NO":
                block = blockAtPos(allJunctions[3].pos + vector(0, 0, sideLength))
                inWires.append(block.wir)
            elif blockAtPos(allJunctions[3].pos + vector(-1*sideLength, 0, 0)) != "NO":
                block = blockAtPos(allJunctions[3].pos + vector(-1*sideLength, 0, 0))
                outWires.append(block.wir)
                
        
        for wire in inWires:
            kcl[wire-1] = -1
        for wire in outWires:
            kcl[wire-1] = 1
        allKCLS.append(kcl)


    if len(allJunctions) > 4:
        junctionsToKCL = allJunctions[4:]
        for junction in junctionsToKCL:
            inWires = []
            outWires = []
            
            kcl = []
            for j in range(listSize):
                kcl.append(0)
            
            directsToCheck = [vec(sideLength, 0, 0), vec(-1*sideLength, 0, 0), vec(0, 0, sideLength), vec(0, 0, -1*sideLength)]
            findBlocks = []
            
            juncPos = junction.pos
            
            for direct in directsToCheck:
                if blockAtPos(juncPos + direct) != "NO":
                    block = blockAtPos(juncPos + direct)
                    findBlocks.append(block)
                    
            if juncPos.x < allJunctions[0].pos.x:
                #"left" of the circuit in the -x direction
                if juncPos.z == allJunctions[0].pos.z:
                    for block in findBlocks:
                        if block.pos.z > juncPos.z:
                            inWires.append(block.wir)
                        elif block.pos.x < juncPos.x:
                            inWires.append(block.wir)
                        elif block.pos.x > juncPos.x:
                            outWires.append(block.wir)
                elif juncPos.z == allJunctions[3].pos.z:
                    for block in findBlocks:
                        if block.pos.x > juncPos.x:
                            inWires.append(block.wir)
                        elif block.pos.x < juncPos.x:
                            outWires.append(block.wir)
                        elif block.pos.z < juncPos.z:
                            outWires.append(block.wir)
            elif juncPos.x > allJunctions[1].pos.x:
                #"right" of the circuit in the x direction
                if juncPos.z == allJunctions[0].pos.z:
                    for block in findBlocks:
                        if block.pos.x < juncPos.x:
                            inWires.append(block.wir)
                        elif block.pos.x > juncPos.x:
                            outWires.append(block.wir)
                        elif block.pos.z > juncPos.z:
                            outWires.append(block.wir)
                elif juncPos.z == allJunctions[3].pos.z:
                    for block in findBlocks:
                        if block.pos.x < juncPos.x:
                            outWires.append(block.wir)
                        elif block.pos.x > juncPos.x:
                            inWires.append(block.wir)
                        elif block.pos.z < juncPos.z:
                            inWires.append(block.wir)
            elif juncPos.z < allJunctions[0].pos.z:
                #"up" of the circuit in the -z direction
       #         print("hello")

                if juncPos.x == allJunctions[0].pos.x:
                    for block in findBlocks:
                        if block.pos.z > juncPos.z:
                            inWires.append(block.wir)
                        elif block.pos.z < juncPos.z:
                            outWires.append(block.wir)
                        elif block.pos.x > juncPos.x:
                            outWires.append(block.wir)
                elif juncPos.x == allJunctions[1].pos.x:
                    for block in findBlocks:
                        if block.pos.x < juncPos.x:
                            inWires.append(block.wir)
                        elif block.pos.z < juncPos.z:
                            inWires.append(block.wir)
                        elif block.pos.z > juncPos.z:
                            outWires.append(block.wir)
            elif juncPos.z > allJunctions[3].pos.z:
                #"down" of the circuit in the z direction
                if juncPos.x == allJunctions[0].pos.x:
                    for block in findBlocks:
                        if block.pos.x > juncPos.x:
                            inWires.append(block.wir)
                        elif block.pos.z > juncPos.z:
                            inWires.append(block.wir)
                        elif block.pos.z < juncPos.z:
                            outWires.append(block.wir)
                elif juncPos.x == allJunctions[1].pos.x:
                    for block in findBlocks:
                        if block.pos.z < juncPos.z:
                            inWires.append(block.wir)
                        elif block.pos.z > juncPos.z:
                            outWires.append(block.wir)
                        elif block.pos.x < juncPos.x:
                            outWires.append(block.wir)
            
            for wire in inWires:
                kcl[wire-1] = -1
            for wire in outWires:
                kcl[wire-1] = 1
                

            allKCLS.append(kcl)
#    for idx, kcl in enumerate(allKCLS):
#        print(f"KCL equation {idx}: {kcl}")        
    return allKCLS

def swap_block(event):
    global highlightBoxes
    global allWires
    global allEMF
    global allResistors
    global circuitBuild
    global is_running
    if is_running:
   #     print("Busy! Wait for the current operation to finish.")
        return
    is_running = True
    try:
        key = event.key
        if circuitBuild == False and len(highlightBoxes) > 0:
            boxToSwap = blockAtPos(highlightBoxes[len(highlightBoxes)-1].pos)
            
            if boxToSwap.pos == allCircuitLoops[0][1].pos:
                return
            
            if key == "s":
                for emf in allEMF:
                    if emf[0].center == boxToSwap.pos:
                        emf[0].visible = False
                        emf[1].visible = False
        #        print("Swap Direction!")
                if boxToSwap.element == "EMF":
                    direction = boxToSwap.directionIn[0]
                    orientation = boxToSwap.flow
                    if orientation == "posToNeg":
                        orientation = "negToPos"
                        boxToSwap.voltage = -1 * boxToSwap.voltage
                        boxToSwap.flow = "negToPos"
                    else:
                        orientation = "posToNeg"
                        boxToSwap.voltage = -1 * boxToSwap.voltage
                        boxToSwap.flow = "posToNeg"
                    if len(direction) > 1:   
                        direction = direction[1]
                    draw_emf(boxToSwap, orientation, direction)
            elif key == 'w' or key == 's' or key == 'r' or key == 'e':
                for wire in allWires:
                    if wire.center == boxToSwap.pos:
                        wire.visible = False
                
                for emf in allEMF:
                    if emf[0].center == boxToSwap.pos:
                        emf[0].visible = False
                        emf[1].visible = False
                        
                for resistor in allResistors:
                    if resistor.center == boxToSwap.pos:
                        resistor.visible = False
                
                if key == 'w':
          #          print("Wire swap!")
                    boxToSwap.voltage = 0
                    boxToSwap.resistance = 0
                    boxToSwap.element = "Wire"
                    direction = boxToSwap.directionIn[0]
                    if len(direction) > 1:
                        direction = direction[1]
           #         print(f"{direction} test direction")
                    draw_wire(boxToSwap, direction)
                elif key == "r":
            #        print("Resistor swap!")
                    boxToSwap.element = "Resistor"
                    boxToSwap.resistance = 2
                    boxToSwap.voltage = 0
                    direction = boxToSwap.directionIn[0]
                    if len(direction) > 1:
                        direction = direction[1]
                    draw_resistor(boxToSwap, direction)
                    
                elif key == "e":
           #         print("EMF swap!")
                    boxToSwap.element = "EMF"
                    boxToSwap.voltage = 10
                    boxToSwap.resistance = 0
                    boxToSwap.flow = "posToNeg"
                    direction = boxToSwap.directionIn[0]
                    orientation = "posToNeg"
                    if len(direction) > 1:   
                        direction = direction[1]
                        orientation = "negToPos"
                    draw_emf(boxToSwap, orientation, direction)
                    
    finally:
        is_running = False
        if wireHighlight[0].visible:
            hideWires()
            showWires()
        if len(highlightBoxes) > 1:
            highlightBoxes[-1].visible = False
        if len(wireHighlightLabels) > 1:
            wireHighlightLabels[-1].visible = False

        
        
scene.bind('keydown', swap_block)
    
def lockCircuit():
    global circuitBuild
    global is_running
    scene.userspin = True
    
    if is_running:
    #    print("Busy! Wait for the current operation to finish.")
        return
    is_running = True
    try:
        circuitBuild = False
    finally:
        is_running = False
    
def unlockCircuit():
    global circuitBuild
    global is_running
    
 #   wireHighlight[-1].visible = False
    wireHighlightLabels[-1].visible = False
    
    scene.userspin = False
    scene.camera.pos = vec(-0.486395, 610.798, 3.87329e-4)
    scene.camera.axis = vec(0.486395, -610.798, -3.87329e-4)
    if is_running:
     #   print("Busy! Wait for the current operation to finish.")
        return
    is_running = True
    try:
        circuitBuild = True
    finally:
        is_running = False

def showKVL():
    global kvlLoops
    for loop in kvlLoops:
        loop.visible = True
    
def hideKVL():
    global kvlLoops
    for loop in kvlLoops:
        loop.visible = False

def showJunc():
    global junctionHighlight
    for junc in junctionHighlight:
        junc.visible = True
    
def hideJunc():
    global junctionHighlight
    for junc in junctionHighlight:
        junc.visible = False
 
def findLabel(position):
    global wireLabels
    for lab in wireLabels:
        if lab.pos == position:
            return int(lab.text)
    return "NO"

def specialModeEnable():
    global allCircuitLoops
    global specialMode
    specialMode = True

    for loop in allCircuitLoops:
        for element in loop:
            element.texture = img_url

def specialModeDisable():
    global allCircuitLoops
    global specialMode
    specialMode = False
    
    for loop in allCircuitLoops:
        for element in loop:
            element.texture = None

def showWires():
    global wireHighlight
    global dimension
    global wireLabels
    hideWires()
    
    matrix = kclCalculate()
    
    kvlLoops = kvlCalculate()
    for loop in kvlLoops:
        matrix.append(loop)
    
    currents = rref(matrix)

    extractedCurrents = []
    
    for i in range(len(actualAllWires)):
        extractedCurrents.append(currents[i][len(actualAllWires)])
    
 #   print(extractedCurrents)
    
    
    wireCount = 1
    for count, wire in enumerate(wireHighlight):
        wire.visible = True
        if (count - (dimension-2)/2) % (dimension-2) == 0:
            lab = label(
                canvas=scene,
                pos=wire.pos + vector(0, sideLength*1.5, 0), 
                text=f"Wire {wireCount} \n Current: {round(extractedCurrents[wireCount-1], 2)} A",
#                text=f"Wire {wireCount} :: Current: Fixing the KVLs",
                xoffset=0, yoffset=0, space=30,
                height=16, border=2, font='sans'
                )
            wireLabels.append(lab)
            wireCount += 1
        
#        block = findClosestBlock(wire.pos)
#        lab = label(
#                canvas=scene,
#                pos=wire.pos + vector(0, sideLength*1.5, 0), 
#                text=f"Wire Count: {block.wir}",
#                xoffset=0, yoffset=0, space=30,
#                height=16, border=2, font='sans'
#                )    
    
    


def hideWires():
    global wireHighlight
    global dimension
    global wireLabels
    
    for wire in wireHighlight:
        wire.visible = False

    for lab in wireLabels:
        lab.pos = vector(1e10, 1e10, 1e10)
        del lab
    
line = "\u2500" * 100 + "\n"
scene.append_to_caption("Note to user: When clicking specific blocks to see specific circuit elements, you may need to reclick to see updated values \n\n")
scene.append_to_caption("Circuit Keybind Manipulation Instructions\n")
scene.append_to_caption(line)

scene.append_to_caption("Once the circuit building is disabled, you may click on blocks to adjust the circuit element:\n")
scene.append_to_caption("[w] - Swap Element to Wire\n")
scene.append_to_caption("[e] - Swap Element to EMF Device\n")
scene.append_to_caption("[r] - Swap Element to Resistor\n")
scene.append_to_caption("[s] - Swap Direction of EMF Device\n\n")

scene.append_to_caption("Circuit Building Controls\n")
    
scene.append_to_caption(line)
scene.append_to_caption("Disable circuit building in order to enable manual swapping of circuit elements and voltages/resistance adjustments. You can do this by clicking on the blocks you wish to manipulate \n")
button(text="Disable Circuit Buliding", bind=lockCircuit)
scene.append_to_caption("\n\n")
scene.append_to_caption("Enable circuit building in order to extend the circuit (click on/near the extended arrows on the exterior circuit sides) \n")
button(text="Enable Circuit Building", bind=unlockCircuit)

create_initial_circuit()

scene.append_to_caption("\n\n")

scene.append_to_caption("Visibility Controls:\n")
scene.append_to_caption(line)
button(text="Show Junctions", bind=showJunc)
scene.append_to_caption("  ")
button(text="Hide Junctions", bind=hideJunc)
scene.append_to_caption("  ")
button(text="Show KVL Loops", bind=showKVL)
scene.append_to_caption("  ")
button(text="Hide KVL Loops", bind=hideKVL)

scene.append_to_caption("\n\n")

button(text="Show Wires and Currents", bind=showWires)
scene.append_to_caption("    ")
button(text="Hide Wires and Currents", bind=hideWires)
scene.append_to_caption("    ")
button(text="Sharaf Mode Enable", bind=specialModeEnable)
scene.append_to_caption("    ")
button(text="Sharaf Mode Disable", bind=specialModeDisable)
scene.append_to_caption("\n\n")



scene.append_to_caption("Adjust resistance or voltage of selected element:\n")

min_val = 1
max_val = 20

scene.append_to_caption(f"{min_val} (magnitude)")
my_slider = slider(min=min_val, max=max_val, step=1, bind=adjustElementValue)
scene.append_to_caption(f" {max_val} (magnitude)\n")
val_text = wtext(text=f"Current Value: {my_slider.value}\n")

scene.append_to_caption("\n\n")


# ELEMENTARY ROW OPERATIONS
def scaleRow(matrix, rowIndex, scalar):
    for count, num in enumerate(matrix[rowIndex]):
        matrix[rowIndex][count] = num*scalar
    return matrix
    
def interChangeRow(matrix, index1, index2):
    row1 = matrix[index1][:]
    matrix[index1] = matrix[index2]
    matrix[index2] = row1[:]
    return matrix

def addRow(matrix, toMatrix, fromMatrix):
    for count, num in enumerate(matrix[fromMatrix]):
        matrix[toMatrix][count] += num
    return matrix

# Checking for 1 to be the pivot
def checkPivotOne(matrix, rowIndex):
    # all entries before the diagonal must be 0
    for i in range(rowIndex):
        if matrix[rowIndex][i] != 0:
            return False
    return matrix[rowIndex][rowIndex] == 1

    
# CODE TO RREF

def is_all_zero(row):
    return all(x == 0 for x in row)
    
def rref(matrix):
    rowCompleted = 0
    while rowCompleted < len(matrix):        
        if is_all_zero(matrix[len(matrix)-1]):
            return matrix
            
        alreadyAdd = False

        if len(matrix) == 1:
            return "Enter more than one row bro..."
        if rowCompleted > len(matrix[0])-2:
            return matrix[0:rowCompleted]
            
        # if pivot is non zero
        if matrix[rowCompleted][rowCompleted] != 0:
            matrix = scaleRow(matrix, rowCompleted, 1 / matrix[rowCompleted][rowCompleted])

        # if pivot is 0, then make it nonzero
        elif matrix[rowCompleted][rowCompleted] == 0:
            swapRow = rowCompleted
            while matrix[rowCompleted][rowCompleted] == 0:
                matrix = interChangeRow(matrix, rowCompleted, swapRow)
                swapRow += 1
                if swapRow > len(matrix):
                    return "Ethan doesn't want to RREF this!"
                    
            if matrix[rowCompleted][rowCompleted] != 0:
                matrix = scaleRow(matrix, rowCompleted, 1/matrix[rowCompleted][rowCompleted])

        originalRow = matrix[rowCompleted][:]

        for count, row in enumerate(matrix):
            if count != rowCompleted:
                matrix = scaleRow(matrix, rowCompleted, -1*row[rowCompleted])
                matrix = addRow(matrix, count, rowCompleted)
                
                matrix[rowCompleted] = originalRow[:]
                
        rowCompleted += 1 
    #    print(matrix)
    return matrix
            

# Common graphing function setup
def setup_graph(title, ytitle, curve_color):
    g = graph(title=title, xtitle="Time (s)", ytitle=ytitle)
    return gcurve(graph=g, color=curve_color)


## 2D - RC Charging Circuit Simulation

scene1 = canvas(width=1200, height=600)
scene1.circuit_built = False
scene1.dielectric_built = False

# === Globals ===
C1 = None
C2 = None
dielectric = None
wire_top = None
wire_bottom = None
plate_area = 1.0
plate_sep = 0.5
grid = 1
switch_closed = False
switch_wire = None
switch_gap = None
switch_arm = None
a1 = None
l1 = None
a2 = None
l2 = None
a3 = None
l3 = None
wire_top = None
wire_bottom = None
R = None
C = None
V = None
voltage_curve = None
current_curve = None
charge_curve = None
voltage_curve_r = None
current_curve_r = None

def clear_previous_circuit():
    global C1, C2, dielectric, wire_top, wire_bottom
    if C1:
        C1.visible = False
    if C2:
        C2.visible = False
    if dielectric:
        dielectric.visible = False
    if wire_top:
        wire_top.visible = False
    if wire_bottom:
        wire_bottom.visible = False

    C1 = C2 = dielectric = wire_top = wire_bottom = None

    
def draw_circuit(include_dielectric=False):
    global C1, C2, dielectric, wire_top, wire_bottom, switch_arm
    clear_previous_circuit()

    wire_radius = 0.05
    comp_width = 0.3
    switch_y = 2 * grid
    
    # Battery 1
    battery1 = box(pos=vector(-6*grid, 0, 0), length=comp_width, height=1.5*grid, width=0.1, color=color.red)
    label(pos=battery1.pos + vector(0, -1*grid, 0), text="ε₁", box=False)

    # Vertical wire from battery to top segment
    cylinder(pos=vector(-6*grid, 0.75*grid, 0), axis=vector(0, 1.25*grid, 0), radius=wire_radius)

    # Continuous vertical wire through battery
    cylinder(pos=vector(-6*grid, -2*grid, 0), axis=vector(0, 4*grid, 0), radius=wire_radius)
    
    # Continuous bottom wire from battery to middle loop
    cylinder(pos=vector(-6*grid, -2*grid, 0), axis=vector(6*grid, 0, 0), radius=wire_radius)

    if switch_arm == None:
       switch_base = box(pos=vector(-2*grid, 2*grid, 0), size=vector(0.2*grid, 0.05*grid, 0.2*grid), color=color.gray(0.5))
       #switch_arm = cylinder(pos=vector(-2*grid, 2*grid, 0), axis=vector(1*grid, 0.3*grid, 0), radius=0.05*grid, color=color.yellow)
       #switch_arm.axis = vector(1*grid, 0.4*grid, 0)
       switch_arm = cylinder(pos=vector(-3*grid, 2*grid, 0), axis=vector(1*grid, 0, 0), radius=0.05*grid, color=color.yellow)
       cylinder(pos=vector(-2*grid + 0.6*grid, 2*grid, 0), axis=vector(1*grid - 0.6*grid, 0, 0), radius=wire_radius)

    # Continuous top wire from battery (+) to loop
    cylinder(pos=vector(-6*grid, 2*grid, 0), axis=vector(3*grid, 0, 0), radius=wire_radius)
    cylinder(pos=vector(-2*grid, 2*grid, 0), axis=vector(2*grid, 0, 0), radius=wire_radius)
    
    # Vertical wires to capacitor
    cylinder(pos=vector(0, 2*grid, 0), axis=vector(0, -plate_sep - 0.1, 0), radius=wire_radius)
    cylinder(pos=vector(0, -2*grid, 0), axis=vector(0, plate_sep + 0.1, 0), radius=wire_radius)

    # === MIDDLE BRANCH ===
    label(pos=vector(0, 2.3*grid, 0), text="a", box=False)
    label(pos=vector(0, -2.3*grid, 0), text="b", box=False)

    # Capacitor plates
    C1 = box(pos=vector(0, plate_sep, 0), length=plate_area, height=0.1, width=plate_area, color=color.green)
    C2 = box(pos=vector(0, -plate_sep, 0), length=plate_area, height=0.1, width=plate_area, color=color.green)

    # Wire from junction a to top capacitor plate
    wire_top = cylinder(pos=vector(0, 2*grid, 0), axis=vector(0, -2*grid + plate_sep + 0.05, 0), radius=wire_radius)

    # Wire from bottom capacitor plate down and back up to junction b
    wire_bottom = cylinder(pos=vector(0, -plate_sep - 0.05, 0), axis=vector(0, -0.95, 0), radius=wire_radius)

    # === RIGHT LOOP ===

    # Top-right resistor
    R3 = box(pos=vector(4*grid, 2*grid, 0), length=2*grid, height=0.3, width=0.1, color=color.orange)

    # Top-right horizontal wiring
    cylinder(pos=vector(1*grid, 2*grid, 0), axis=vector(5*grid, 0, 0), radius=wire_radius)

    # Bottom-right horizontal wire
    cylinder(pos=vector(6*grid, -2*grid, 0), axis=vector(-6*grid, 0, 0), radius=wire_radius)

    # Continuous right battery wire (from bottom to top)
    cylinder(pos=vector(6*grid, -2*grid, 0), axis=vector(0, 4*grid, 0), radius=wire_radius)

    # Wire from junction a to start of right loop
    cylinder(pos=vector(0, 2*grid, 0), axis=vector(1*grid, 0, 0), radius=wire_radius)
    
    # === DIELECTRIC ===
    if include_dielectric:
        dielectric = box(
        pos=vector(0, 0, 0),
        length=C1.length,
        height=abs(C1.pos.y - C2.pos.y),
        width=C1.width,
        opacity=0.5,
        color=color.cyan
        )
        label(
        pos=dielectric.pos + vector(0.5, 0, 0),
        text="Dielectric",
        height=10,
        box=False,
        color=color.cyan
        )


def build_standard(evt):
    # print("Build 2D RC Circuit clicked!") 
    if not scene1.circuit_built:
        scene1.circuit_built = True
    draw_circuit(include_dielectric=False)
    global a1, l1, a2, l2, a3, l3
    # === Current Arrows ===
#    a1 = arrow(pos=vector(-7*grid, 0, 0), axis=vector(0, 2, 0), shaftwidth=0.1, color=color.green)
#    l1 = label(pos=vector(-7*grid, 1.2*grid, 0), text="I₁", color=color.green, box=False)
#
#    a2 = arrow(pos=vector(7*grid, 0, 0), axis=vector(0, 1, 0), shaftwidth=0.1, color=color.green)
#    l2 = label(pos=vector(7*grid, 1.2*grid, 0), text="I₂", color=color.green, box=False)
#
#    a3 = arrow(pos=vector(0, 2*grid, 0), axis=vector(0, -1, 0), shaftwidth=0.1, color=color.green)
#    l3 = label(pos=vector(0.6*grid, 0.7*grid, 0), text="I₃", color=color.green, box=False)
#    
#    a1.axis = vector(0, 0, 0)
#    a2.axis = vector(0, 0, 0)
#    a3.axis = vector(0, 0, 0)
#    l1.color = color.black
#    l2.color = color.black
#    l3.color = color.black
    
    
def build_dielectric(evt):
    if not scene1.dielectric_built:
        scene1.dielectric_built = True
    draw_circuit(include_dielectric=True)


#def calculate_capacitance():
#    global plate_area, plate_sep, scene1
#    epsilon_0 = 8.85e-12
#    epsilon_r = 1
#    epsilon_r_dielectric = 4  # example dielectric constant
#
#    A = plate_area ** 2
#    d = plate_sep
#    er = epsilon_r_dielectric if scene1.dielectric_built else epsilon_r
#    return epsilon_0 * er * A / d

def update_area(s):
    global C1, C2, dielectric, plate_area
    plate_area = s.value * s.value
    if C1 and C2:
        C1.length = s.value
        C1.width = s.value
        C2.length = s.value
        C2.width = s.value
    if dielectric:
        dielectric.length = s.value
        dielectric.width = s.value

def update_separation(s):
    global C1, C2, dielectric, wire_top, wire_bottom, plate_sep
    sep = s.value
    plate_sep = sep * 2
    
    if C1 and C2:
     #   print(plate_sep)
        C1.pos.y = sep
        C2.pos.y = -sep

    if dielectric:
        dielectric.height = abs(C1.pos.y - C2.pos.y)
        dielectric.pos.y = (C1.pos.y + C2.pos.y) / 2

    if wire_top and C1:
        wire_top.pos = vector(C1.pos.x, C1.pos.y, C1.pos.z)
        wire_top.axis = vector(0, 2 - sep, 0)   

    if wire_bottom and C2:
        wire_bottom.pos = vector(C2.pos.x, C2.pos.y, C2.pos.z)
        wire_bottom.axis = vector(0, -2 + sep, 0) 
    
    
# === Interface ===
# button(canvas=scene1, text="Build 2D RC Circuit", bind=build_standard)
build_standard()

scene1.append_to_caption("Note to User: Press this button to fill the capacitor plates with a dielectric.")
button(canvas=scene1, text="Build RC Circuit with Dielectric", bind=build_dielectric)

scene1.append_to_caption("\n\nArea of Capacitor: ")
slider_area = slider(canvas=scene1, bind=update_area, min=0.2, max=2.0, value=1.0, step=0.1)

scene1.append_to_caption("\n\nSeparation Distance: ")
plate_sep_slider = slider(canvas=scene1, bind=update_separation, min=0.1, max=1.0, value=plate_sep, step=0.05)
scene1.append_to_caption("\n\n")


# Circuit simulation function (returns all data)
def simulate_RC_data():
    #Update calculations based on slider inputs
    global R, C, V, plate_area, plate_sep, scene1


    plate_area_value = plate_area
    plate_sep_value = plate_sep

    epsilon_0 = 8.85e-12
    epsilon_r = 1
    epsilon_r_dielectric = 4
    A = plate_area_value
    d = plate_sep_value
    er = epsilon_r_dielectric if scene1.dielectric_built else epsilon_r
    C = epsilon_0 * er * A / d 

    R = 5      # Ohms
    V = 10     # Volts

    V0 = V
    q0 = C * V0 
    t = 0
    tFinal = 0.000000002
    dt = tFinal / 100
    Vr = 0

    time_data = []
    charge_data = []
    current_data = []
    voltage_data = []
    voltage_data_r = []
    current_data_r = []

    while t < tFinal:
        q = q0 * (1 - euler()**(-t / (R * C)))
        i = -q0 / (R * C) * euler()**(-t / (R * C))
        Vt = V0 * euler()**(-t / (R * C))
        
        Vr = V0 / R * euler()**(-t / (R * C))
        ir = -V0 / R * euler()**(-t / (R * C))

        time_data.append(t)
        charge_data.append(q)
        current_data.append(i)
        voltage_data.append(Vt)
        voltage_data_r.append(Vr)
        current_data_r.append(ir)

        t += dt
    return time_data, charge_data, current_data, voltage_data, voltage_data_r, current_data_r

    
def open_switch():
    global switch_closed, switch_arm, a1, l1, a2, l2, a3, l3
    
    if not switch_closed:
#        # Closed: bar is flat across the gap
        switch_arm.pos = vector(-2*grid, 2*grid, 0)
        switch_arm.axis = vector(1*grid, 0.4*grid, 0)
    else:
#        # Open: bar is tilted/lifted above
        switch_arm.pos = vector(-3*grid, 2*grid, 0)
        switch_arm.axis = vector(1*grid, 0, 0)
        
def close_switch_back():
    global switch_closed, switch_arm, a1, l1, a2, l2, a3, l3
    
    if switch_closed:
        switch_arm.pos = vector(-2*grid, 2*grid, 0)
        switch_arm.axis = vector(1*grid, 0.4*grid, 0)
    else:
#        # Open: bar is tilted/lifted above
        switch_arm.pos = vector(-3*grid, 2*grid, 0)
        switch_arm.axis = vector(1*grid, 0, 0)

def update_graphs():
    while True:
        clear()
        show_charge_graph()
        show_current_graph()
        show_voltage_graph()
        show_voltage_resistor_graph()
        rate(10)  # Updates every 10 cycles
    
# Individual plot functions
def show_charge_graph(evt=None):
    global is_running, charge_curve
    if is_running:
      #  print("Another plot is running, please wait!")
        return
    is_running = True
    try:
        plate_area_value = slider_area.value
        plate_sep_value = plate_sep_slider.value * 2
        time_data, charge_data, _, _ = simulate_RC_data()

        if charge_curve == None:
            charge_curve = setup_graph("Charge Capacitor vs Time", "Charge (C)", color.blue)
            
        for t, q in zip(time_data, charge_data):
            rate(500)
            charge_curve.plot(t, q)
    finally:
        is_running = False

def show_current_graph(evt=None):
    global is_running, current_curve
    if is_running:
   #     print("Another plot is running, please wait!")
        return
    is_running = True
    try:
        plate_area_value = slider_area.value
        plate_sep_value = plate_sep_slider.value * 2
        time_data, _, current_data, _ = simulate_RC_data(plate_area_value, plate_sep_value)

        if current_curve == None:
            current_curve = setup_graph("Current Capacitor vs Time", "Current (A)", color.red)
        
        for t, i in zip(time_data, current_data):
            rate(500)
            current_curve.plot(t, i)
    finally:
        is_running = False

def show_voltage_graph(evt=None):
    global is_running, voltage_curve
    if is_running:
    #    print("Another plot is running, please wait!")
        return
    is_running = True
    try:
        plate_area_value = slider_area.value
        plate_sep_value = plate_sep_slider.value * 2
        time_data, _, _, voltage_data = simulate_RC_data(plate_area_value, plate_sep_value)
        
        if voltage_curve == None:
            voltage_curve = setup_graph("Voltage Capacitor vs Time", "Voltage (V)", color.green)
            
        for t, V in zip(time_data, voltage_data):
            rate(500)
            voltage_curve.plot(t, V)
    finally:
        is_running = False
        
def show_voltage_resistor_graph(evt=None):
    global is_running, voltage_curve_r
    if is_running:
    #    print("Another plot is running, please wait!")
        return
    is_running = True
    try:
        plate_area_value = slider_area.value
        plate_sep_value = plate_sep_slider.value * 2
        time_data, _, _, _, voltage_data_r = simulate_RC_data()

        
        if voltage_curve_r == None:
            voltage_curve_r = setup_graph("Voltage Resistor vs Time", "Voltage (V)", color.orange)
            
        for t, Vr in zip(time_data, voltage_data_r):
            rate(500)
            voltage_curve_r.plot(t, Vr)
    finally:
        is_running = False

def show_current_resistor_graph(evt=None):
    global is_running, current_curve_r
    if is_running:
    #    print("Another plot is running, please wait!")
        return
    is_running = True
    try:
        plate_area_value = slider_area.value
        plate_sep_value = plate_sep_slider.value * 2
        time_data, _, _, _, _, current_data_r = simulate_RC_data(plate_area_value, plate_sep_value)

        if current_curve_r == None:
            current_curve_r = setup_graph("Current Resistor vs Time", "Current (A)", color.red)
        
        for t, i in zip(time_data, current_data_r):
            rate(500)
            current_curve_r.plot(t, i)
    finally:
        is_running = False

def clear():
    global voltage_curve, current_curve, charge_curve, voltage_curve_r, current_curve_r
    voltage_curve.delete()
    current_curve.delete()
    charge_curve.delete()
    voltage_curve_r.delete()
    current_curve_r.delete()
    
def start_graphs(evt=None):
    clear()
    show_charge_graph()
    show_current_graph()
    show_voltage_graph()
    show_voltage_resistor_graph()
    show_current_resistor_graph()

    
# Buttons
button(canvas=scene1, text="Open Switch", bind=open_switch)
button(canvas=scene1, text="Close Switch", bind=close_switch_back)
scene1.append_to_caption("\n")
scene1.append_to_caption("Pressing the below button will show the graphs \n")
button(canvas=scene1, text="Start Graphs", bind=start_graphs)
scene1.append_to_caption("\n")
scene1.append_to_caption("Pressing the below button will reset the graphs. During this time, you may adjust the sliders \n")
button(canvas=scene1, text="Clear Graphs", bind=clear)
