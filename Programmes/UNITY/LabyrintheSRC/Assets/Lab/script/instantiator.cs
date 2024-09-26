using UnityEngine;

public class instantiator : MonoBehaviour
{
    public GameObject objetAInstancier;
    public int nombreColonnes;
    public int nombreLignes;
    public float espacementX;
    public float espacementY;
    [SerializeField]
    public GameObject objetAActiver;

    void Start()
    {
        CreerGrille();
        objetAActiver.SetActive(true);
    }

    void CreerGrille()
    {
        for (int i = 0; i < nombreColonnes; i++)
        {
            for (int j = 0; j < nombreLignes; j++)
            {
                Vector3 position = new Vector3(((float)i + 1f/2f) * espacementX, 0f, ((float)j + 1f/2f) * espacementY);
                GameObject newInstance =Instantiate(objetAInstancier, position, Quaternion.identity);
                newInstance.name = $"{i},{j}";

            }
        }
    }
}
