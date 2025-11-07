import jawm

multiqc_submodule_p1=jawm.Process( 
    name="multiqc_submodule_p1",
    script="""#!/bin/bash
echo "Demo module echo process"
"""  
)