using UnityEngine;

public class EdgeController : MonoBehaviour
{
    private Transform _startTransform;
    private Transform _endTransform;
    private LineRenderer _lineRenderer;
    
    public void SetNodeControllers(NodeController startNode, NodeController endNode)
    {
        _startTransform = startNode.transform;
        _endTransform = endNode.transform;
    }
    
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        _lineRenderer = GetComponent<LineRenderer>();
        UpdateLine();
    }

    // Update is called once per frame
    void Update()
    {
        if (HaveNodesChanged()) UpdateLine();
    }

    private bool HaveNodesChanged()
    {
        return !(_startTransform.position.Equals(_lineRenderer.GetPosition(0))
            && _endTransform.position.Equals(_lineRenderer.GetPosition(1)));
    }

    private void UpdateLine()
    {
        _lineRenderer.SetPosition(0, _startTransform.position);
        _lineRenderer.SetPosition(1, _endTransform.position);
    }
}
