using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using Random = UnityEngine.Random;

public class labgenV2 : MonoBehaviour
{
    public int i; // Champ pour i
    public int j; // Champ pour j
    public int SIZEP;
    public int SIZEQ;
    public int PROB;
    public float hauteur;
    public float hauteurbas;
    public float WaitimeIn;
    public float Waitintertime;

    private Dictionary<Vector2, bool> g;

    void Update()
    {
        Vector2 sta = new Vector2(i, j);
        StartCoroutine(Generate(SIZEP, SIZEQ, i, j));
    }

    private int Adj(int i, int j, Dictionary<Vector2, bool> g)
    {
        int a = 0;
        if (g.ContainsKey(new Vector2(i - 1, j))) a++;
        if (g.ContainsKey(new Vector2(i + 1, j))) a++;
        if (g.ContainsKey(new Vector2(i, j - 1))) a++;
        if (g.ContainsKey(new Vector2(i, j + 1))) a++;
        return a;
    }

    private bool Possible(int i, int j, int p, int q, Dictionary<Vector2, bool> g)
    {
        return i >= 0 && j >= 0 && i <= p && j <= q && !g.ContainsKey(new Vector2(i, j)) && Adj(i, j, g) == 1;
    }

    private IEnumerator Generate(int p, int q, int Ie, int Je)
    {
        string name = "";
        GameObject foundObject = null;

        for (int i = 0; i < p; i++) // Reset la grille
        {
            for (int j = 0; j < q; j++)
            {
                if (!(i == Ie && j == Je))
                {
                    name = i.ToString() + "," + j.ToString();
                    foundObject = GameObject.Find(name);
                    if (foundObject != null)
                    {
                        Transform objectTransform = foundObject.transform;
                        objectTransform.position = new Vector3(objectTransform.position.x, hauteur, objectTransform.position.z);
                    }
                }
            }
        }

        List<Vector2> cu = new List<Vector2>();
        List<Vector2> nxt = new List<Vector2>();
        Dictionary<Vector2, bool> g1 = new Dictionary<Vector2, bool>();

        g1[new Vector2(Ie, Je)] = true;

        if (Possible(Ie, Je + 1, p, q, g1))
        {
            nxt.Add(new Vector2(Ie, Je + 1));
        }
        if (Possible(Ie, Je - 1, p, q, g1))
        {
            nxt.Add(new Vector2(Ie, Je - 1));
        }
        if (Possible(Ie + 1, Je, p, q, g1))
        {
            nxt.Add(new Vector2(Ie + 1, Je));
        }
        if (Possible(Ie - 1, Je, p, q, g1))
        {
            nxt.Add(new Vector2(Ie - 1, Je));
        }

        while (nxt.Count != 0)
        {
            cu = new List<Vector2>(nxt);
            nxt.Clear();

            foreach (var k in cu)
            {
                int i = (int)k.x;
                int j = (int)k.y;

                if (Possible(i, j, p, q, g1) && Random.Range(0, PROB) == 1)
                {
                    g1[new Vector2(i, j)] = true;
                    name = i.ToString() + "," + j.ToString();
                    foundObject = GameObject.Find(name);
                    if (foundObject != null)
                    {
                        Transform objectTransform = foundObject.transform;
                        objectTransform.position = new Vector3(objectTransform.position.x, hauteurbas, objectTransform.position.z);
                        yield return new WaitForSeconds(WaitimeIn);
                    }

                    if (Possible(i, j + 1, p, q, g1))
                        nxt.Add(new Vector2(i, j + 1));
                    if (Possible(i, j - 1, p, q, g1))
                        nxt.Add(new Vector2(i, j - 1));
                    if (Possible(i + 1, j, p, q, g1))
                        nxt.Add(new Vector2(i + 1, j));
                    if (Possible(i - 1, j, p, q, g1))
                        nxt.Add(new Vector2(i - 1, j));
                }
                else
                {
                    if (Possible(i, j, p, q, g1))
                        nxt.Add(new Vector2(i, j));
                }
            }
        }
        yield return new WaitForSeconds(Waitintertime);
    }
}
