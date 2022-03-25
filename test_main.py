from main import subwayNetwork
import pytest

@pytest.mark.parametrize(
    "networkFile,initialNode,finalNode, typeStation, expected",
    [
        ('networkTopololy.json','A','F','','Shortest path = A->B->C->D->E->F'),
        ('networkTopololy.json','A','F','red','Shortest path = A->B->C->H->F'),
        ('networkTopololy.json','a','f','','Out-of-route stations, check network topology'),
        ('networkTopololy.json','A','H','green','Out-of-route stations, check network topology'),
        ('networkTopololy.json','A','H','blue','Wrong train color, available green and red'),
        ('','A','F','','Empty path, apparently the topology file was not loaded'),
        ('jiro.json','A','F','','Empty path, apparently the topology file was not loaded')
    ]
)
def test_subwayNetwork(networkFile,initialNode,finalNode, typeStation, expected):
    var = subwayNetwork(networkFile)
    assert var.findShortestPath(initialNode,finalNode, typeStation) == expected
    
