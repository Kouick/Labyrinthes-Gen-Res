using UnityEngine;

public class edit : MonoBehaviour
{
    public bool isLevered; // État actuel du levier

    // Méthode appelée lors de l'événement
    public void OnEventTriggered(bool eventParameter)
    {
        // Si les valeurs sont identiques, ne rien faire
        if ((eventParameter && isLevered) || (!eventParameter && !isLevered))
        {
            Debug.Log("Les valeurs sont identiques. Rien ne change.");
            return;
        }

        // Si les valeurs sont différentes, mettre à jour l'état du levier
        isLevered = eventParameter;

        // Effectuer l'action correspondante (lever ou baisser le GameObject)
        if (isLevered)
        {
            LeverGameObject();
        }
        else
        {
            BaisserGameObject();
        }
    }

    // Méthode pour lever le GameObject
    private void LeverGameObject()
    {
        Debug.Log("Levage du GameObject.");
        // Mettez ici le code pour lever le GameObject.
    }

    // Méthode pour baisser le GameObject
    private void BaisserGameObject()
    {
        Debug.Log("Baisse du GameObject.");
        // Mettez ici le code pour baisser le GameObject.
    }
}
