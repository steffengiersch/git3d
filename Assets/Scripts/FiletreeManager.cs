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
        GenerateNodes(_root.filetree.AsChild(), null, 0, 0);
    }

    private int GenerateNodes(Child node, NodeController parentNode, int depth, int breadth)
    {
        var childNode = InstantiateNode(depth, breadth, node.name);
        if (parentNode != null) InstantiateLine(parentNode, childNode);

        if (node.children == null || node.children.Count == 0) return breadth + 1;
        
        int currentBreadth = breadth;
        foreach(var child in node.children)
        {
            currentBreadth = GenerateNodes(child, childNode, depth + 1, currentBreadth);
        }
        
        return currentBreadth;
    }

    private NodeController InstantiateNode(int depth, int breadth, string instanceName)
    {
        var instance = Instantiate(nodePrefab, new Vector3(2f * depth, 0f, 2f * breadth), Quaternion.identity, transform);
        instance.name = instanceName;
        instance.nodeName = instanceName;
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
    
    [System.Serializable]
    public class Child
    {
        public string type;
        public string name;
        public string created;
        public string lastModified;
        public int changes;
        public int sizeInByte;
        public double criticality;
        public List<Contributer> contributer;
        public List<Child> children;
        public string extension;
    }

    [System.Serializable]
    public class Contributer
    {
        public string id;
        public string name;
        public double knowledge;
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
        public double criticality;
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
