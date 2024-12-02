import numpy as np
from scipy.interpolate import interp1d



def findImpactPoint(coordinates): #debugged
    setupY = coordinates[0][1]
    for i, (x, y) in enumerate(coordinates):
        if y < setupY:
            return coordinates[i]

def analyzePuttingStroke(coordinates):
    xCoordinates = [coord[0] for coord in coordinates]
    yCoordinates = [coord[1] for coord in coordinates]
    
    impactPoint = findImpactPoint(coordinates)
    impactIndex = coordinates.index(impactPoint)
    
    def calculateArcQuality(x, y):
        xN = np.array(xCoordinates)
        yN = np.array(yCoordinates)

        x_norm = (xN - xN.mean()) / xN.std()
        y_norm = (yN - yN.mean()) / yN.std()

        quadratic = np.polyfit(x_norm, y_norm, 2)
        arcHeight = abs(quadratic[0])
        idealMinArc, idealMaxArc = 0.25, 0.7
        # print('Quadratic: ' + quadratic)
        print('Arc Height' + str(arcHeight))
        if arcHeight < idealMinArc:
            return 100 - (idealMinArc - arcHeight) * 500
        elif arcHeight > idealMaxArc:
            return 100 - (arcHeight - idealMaxArc) * 500
        else:
            return 100
        
    
    backswingArcQuality = calculateArcQuality(xCoordinates[:impactIndex], yCoordinates[:impactIndex])
    forwardSwingArcQuality = calculateArcQuality(xCoordinates[impactIndex:], yCoordinates[impactIndex:])
    
    arcConsistency = 100 - abs(backswingArcQuality - forwardSwingArcQuality)
    
    setupPoint = coordinates[0]
    impactDeviation = np.sqrt((impactPoint[0] - setupPoint[0])**2 + (impactPoint[1] - setupPoint[1])**2)
    impactScore = 100 - impactDeviation * 0.5
    
    # backswingPath = interp1d(xCoordinates[:impactIndex], yCoordinates[:impactIndex], kind='quadratic')
    # forwardSwingPath = interp1d(xCoordinates[impactIndex:], yCoordinates[impactIndex:], kind='quadratic')
    # commonX = xCoordinates[:min(impactIndex, len(xCoordinates)-impactIndex)]
    # pathDifference = np.mean(np.abs(backswingPath(commonX) - forwardSwingPath(commonX)))
    # pathScore = 100 - pathDifference * 0.1
    
    overallScore = (
        0.33 * (backswingArcQuality + forwardSwingArcQuality) / 2 +
        0.33 * arcConsistency +
        0.34 * impactScore 
  
    )
    print()
    
    print('Backswing Arc Quality: ' + str(backswingArcQuality))
    print('Forwardswing Arc Quality: ' +str(forwardSwingArcQuality))
    print('Arc consistency: ' +str(arcConsistency))
    print('Impact score: ' +str(impactScore))
    return max(min(overallScore, 100), 0)

# Example usage
coordinates = [(970, 681), 
(962, 693), 
 (964, 711), 
 (966, 725), 
 (962, 751), 
(959, 770), 
(960, 793), 
 (955, 812), 
(952, 827), 
(956, 820), 
(955, 812), 
(961, 788), 
(970, 757), 
(966, 720), 
(969, 679), 
(967, 646),
(966, 622), 
(969, 603), 
(966, 594), 
(967, 588),
(965, 590)]

coordinates = [(1042, 732), (1043, 756), (1069, 748), (1057, 787), (1070, 808), (1055, 822), (1067, 834), (1060, 837), (1057, 845), (1051, 830), (1033, 796), (1038, 730), (1032, 688), (1014, 630)]

coordinates = [(1090, 683), (1091, 690), (1091, 700), (1085, 710), (1088, 728), (1088, 750), (1090, 778), (1092, 801), (1092, 818), (1094, 833), (1090, 829), (1088, 817), (1097, 794), (1089, 762), (1095, 724), (1082, 680), (1082, 646), (1079, 618), (1074, 598), (1075, 587), (1079, 579)]
# coordinates = [(970, 681), 
# (962, 693), 
#  (964, 711), 
#  (966, 725), 
#  (962, 751), 
# (959, 770), 
# (960, 793), 
#  (955, 812), 
# (952, 827), 
# (956, 820), 
# (955, 812), 
# (961, 788), 
# (970, 757), 
# (966, 720), 
# (969, 679), 
# (967, 646),
# (966, 622), 
# (969, 603), 
# (966, 594), 
# (967, 588),
# (965, 590)]

# coordinates = [(969, 680), (966, 692), (963, 707), (962, 725), (960, 743), (954, 773), (958, 797), (957, 809), (953, 818), (953, 820), (958, 805), (962, 789), (968, 755), (970, 718), (970, 677), (971, 644), (970, 620), (973, 598), (971, 585), (967, 575)]



score = analyzePuttingStroke(coordinates)
print(f"Putting stroke score: {score:.2f}")
print(f"Impact point: {findImpactPoint(coordinates)}")