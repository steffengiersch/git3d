using System;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using Random = UnityEngine.Random;

public class NodeController : MonoBehaviour
{
    [SerializeField] Renderer Sphere;
    [SerializeField] Material BaseMaterial;
    public string nodeName;
    public float criticality;
    public List<FiletreeManager.Contributer> contributers = new();


    private void Start()
    {
        Debug.Log($"Got color: {contributers[0].color}");
        SetColor();
        Sphere.transform.localScale = Vector3.one * criticality * 2f; // #magic
    }

    private void SetColor()
    {
        var colors = contributers.Select(contributer => contributer.color).ToArray();
        //var lerpedColor = LerpMultipleColors(colors, 0.5f);

        Sphere.material = new Material(BaseMaterial);
        var i = Random.Range(0, colors.Length);
        Sphere.material.color = colors[i];
    }
    
    private Color LerpMultipleColors(Color[] colors, float t)
    {
        if (colors == null || colors.Length == 0)
        {
            throw new System.ArgumentException("No colors provided for interpolation.");
        }

        // Clamp the value to be between 0 and 1
        t = Mathf.Clamp01(t);

        float total = colors.Length - 1;
        float step = 1f / total;

        for (int i = 0; i < total; i++)
        {
            // This determines the thresholds at which to lerp between colors
            if (t < step * (i + 1))
            {
                float localT = (t - step * i) / step;
                return Color.Lerp(colors[i], colors[i + 1], localT);
            }
        }

        return colors[colors.Length - 1]; // t = 1 (or close to it), return the last color
    }
}
