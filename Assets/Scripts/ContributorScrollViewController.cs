using System.Collections.Generic;
using UnityEngine;

public class ContributorScrollViewController : MonoBehaviour
{
    [SerializeField] private UIControbutor uiContributorPrefab; 
    private List<UIControbutor> _uiElements = new();
    
    private void Start()
    {
        FindFirstObjectByType<FiletreeManager>().ContributorsChanged += UpdateContributors;
    }

    private void UpdateContributors(List<FiletreeManager.Contributor> contributors)
    {
        GetComponent<RectTransform>().sizeDelta = new Vector2(0f, 24f * contributors.Count);
        _uiElements.ForEach(element => Destroy(element.gameObject));
        _uiElements = new();

        for (int i = 0; i < contributors.Count; i++)
        {
            _uiElements.Add(InstantiateContributor(contributors[i], i));
        }
    }

    private UIControbutor InstantiateContributor(FiletreeManager.Contributor contributor, int i)
    {
        var instance = Instantiate(uiContributorPrefab, transform);
        instance.SetColor(contributor.color);
        instance.SetText(contributor.name);
        instance.SetListPosition(i);
        return instance;
    }
}
