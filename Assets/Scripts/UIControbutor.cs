using System;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

public class UIControbutor : MonoBehaviour
{
    [SerializeField] private TextMeshProUGUI textElement;
    [SerializeField] private RawImage imageElement;

    public void SetText(string text) => textElement.text = text;
    public void SetColor(Color color) => imageElement.color = color;
    public void SetListPosition(int i) => GetComponent<RectTransform>().localPosition = new Vector3(2f, -1f * i * 24f, 0f);
}
