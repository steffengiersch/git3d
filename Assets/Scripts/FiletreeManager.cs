using System.Collections.Generic;
using UnityEngine;

public class FiletreeManager : MonoBehaviour
{
    [SerializeField] private NodeController nodePrefab;
    [SerializeField] private EdgeController edgePrefab;
    private Root _root;
    private List<NodeController> nodes = new();
    private List<LineRenderer> lines = new();
    
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        ParseJson();
        GenerateColorsForContributors();
        GenerateNodes(_root.filetree.AsChild(), null, 0, 0);
    }

    private void GenerateColorsForContributors()
    {
        var colors = GenerateDistinctColors(_root.contributer.Count);
        Debug.Log("Generated colors");
        colors.ForEach(color => Debug.Log($"{color}"));
        Debug.Log($"Blue: {Color.blue}");
        for (int i = 0; i < _root.contributer.Count; i++)
        {
            _root.contributer[i].color = colors[i];
        }
    }

    private int GenerateNodes(Child node, NodeController parentNode, int depth, int breadth)
    {
        var childNode = InstantiateNode(depth, breadth, node);
        if (parentNode != null) InstantiateLine(parentNode, childNode);

        if (node.children == null || node.children.Count == 0) return breadth + 1;
        
        int currentBreadth = breadth;
        foreach(var child in node.children)
        {
            currentBreadth = GenerateNodes(child, childNode, depth + 1, currentBreadth);
        }
        
        return currentBreadth;
    }

    private NodeController InstantiateNode(int depth, int breadth, Child node)
    {
        var instance = Instantiate(nodePrefab, new Vector3(2f * depth, 0f, 2f * breadth), Quaternion.identity, transform);
        instance.name = node.name;
        instance.nodeName = node.name;
        instance.criticality = node.criticality;
        instance.contributers = node.contributer;
        instance.contributers.ForEach(contributer => contributer.color = _root.contributer.Find(c => contributer.name.Equals(c.name)).color);
        nodes.Add(instance);
        return instance;
    }

    private void InstantiateLine(NodeController parentNode, NodeController childNode)
    {
        var instance = Instantiate(edgePrefab, transform);
        instance.SetNodeControllers(parentNode, childNode);
        instance.name = $"{parentNode.nodeName}_{childNode.nodeName}";
    }
    
    private void ParseJson()
    {
        Debug.Log("Parsing Json");
        string jsonContent = System.IO.File.ReadAllText(Application.dataPath + "/Ressources/dummy.json");
        _root = JsonUtility.FromJson<Root>(jsonContent);
        Debug.Log("Finished parsing Json");
    }
    
    List<Color> GenerateDistinctColors(int numColors)
    {
        List<Color> colors = new List<Color>();
        float hueStep = 1.0f / numColors;

        for (int i = 0; i < numColors; i++)
        {
            float hue = i * hueStep;
            Color color = Color.HSVToRGB(hue, 1.0f, 1.0f);
            colors.Add(color);
        }

        return colors;
    }


    [System.Serializable]
    public class Child
    {
        public string type;
        public string name;
        public string created;
        public string lastModified;
        public int changes;
        public int sizeInByte;
        public float criticality;
        public List<Contributer> contributer;
        public List<Child> children;
        public string extension;
    }

    [System.Serializable]
    public class Contributer
    {
        public string name;
        public float knowledge;
        public Color color;
    }

    [System.Serializable]
    public class Filetree
    {
        public string type;
        public string name;
        public string created;
        public string lastModified;
        public int changes;
        public int sizeInByte;
        public float criticality;
        public List<Contributer> contributer;
        public List<Child> children;
        public Child AsChild()
        {
            return new Child()
            {
                type = type,
                name = name,
                created = created,
                lastModified = lastModified,
                changes = changes,
                sizeInByte = sizeInByte,
                criticality = criticality,
                contributer = contributer,
                children = children
            };
        }
    }

    [System.Serializable]
    public class Repository
    {
        public string name;
        public string url;
    }

    [System.Serializable]
    public class Root
    {
        public Repository repository;
        public List<Contributer> contributer;
        public Filetree filetree;
    }







}
