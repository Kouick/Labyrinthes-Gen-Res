using System.Collections;
using UnityEngine;

public class GOCIBL : MonoBehaviour
{
    public GameObject Cible;
    public bool go;
    private Rigidbody r;
    private float a;

    // Start is called before the first frame update
    void Start()
    {
        r = GetComponent<Rigidbody>();
    }

    // Update is called once per frame
    void Update()
    {
        if (go)
        {
            a = Cible.transform.position.y - transform.position.y;

            if (Mathf.Abs(a) > 0.1f)
            {
                r.velocity = new Vector3(0, a, 0);
            }
        
            else
            {
                r.velocity = Vector3.zero;
                go=false;
            }
        }
    }
}
