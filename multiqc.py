import jawm

multiqc_p1=jawm.Process( 
    name="multiqc_p1",
    script="""#!/bin/bash
echo "{{extra_args}} {{my_multiqc_argument}}" 2>&1 | tee {{output}}/multiqc.txt
""",

    # arguments for the script above :
    
    # var={
    #     "extra_args": "",
    #     "my_multiqc_argument":"This is just a multiqc.", 
    #     "mk.output":"<output_folder>", # the prefix "mk." leads to the creation of this folder and volume mapping if you are using containers
    # },

    # here you can describe your variables
    desc={
        "extra_args": "use this if you want to add not preset arguments",
        "my_multiqc_argument":"Some text that will be printed to the screen.", 
        "output":"Folder for output", # the prefix "mk." leads to the creation of this folder and volume mapping if you are using containers
    },
    
    # example arguments for jawn

    # manager="slurm",
    # manager_slurm={
    #     "-p":"cluster,dedicated", 
    #     "--mem":"20GB", 
    #     "-t":"1:00:00", 
    #     "-c":"8" 
    # },
    
    # container="mpgagebioinformatics/fastqc:0.11.9",
    # environmnent="apptainer",
    # environment_apptainer={ '-B': [input_file, output_folder] }
    
    # environmnent="docker",
    # environment_docker={ '-v': [input_file, output_folder] },

    # param_file="yaml/apptainer.params.yaml" ,
    # param_file=[ "yaml/apptainer.params.yaml" , "yaml/slurm.params.yaml" ],
  
)

multiqc_p2=jawm.Process( 
    name="multiqc_p2",
    script="""#!/usr/bin/env python3
with open("{{map.file}}", "r") as src, open("{{output}}/multiqc.txt", "a") as dst:
    dst.write(src.read())
""",

    # arguments for the script above :
    
    # var={
    #     "mk.output":"<output_folder>", # the prefix "mk." leads to the creation of this folder and volume mapping if you are using containers
    #     "map.file":"<some_file>"# the prefix "map." leads to the mapping of this file if you are using containers
    # },
  
)

multiqc_p3=jawm.Process( 
    name="multiqc_p3",
    script="""#!/usr/bin/env Rscript
write( "\nDemo completed", file = "{{output}}/multiqc.txt", append = TRUE)
""",

    # arguments for the script above :
    
    # var={
    #     "mk.output":"<output_folder>", # the prefix "mk." leads to the creation of this folder and volume mapping if you are using containers
    # },
  
)


if __name__ == "__main__":
    import sys
    from jawm.utils import workflow
    from jawm.utils import load_modules

    # load modules from local folders
    load_modules("submodules")

    # load modules from online git repos
    load_modules("jawm_template")

    # it can be used in the form
    # load_modules(["modules","jawm_template@<tag/commit_hash>"])
    
    # or for latest available tag
    # load_modules("jawm_template@latest")

    workflows, var, args, unknown_args= jawm.utils.parse_arguments(["main","multiqc","test"],)

    # usage: 

    if workflow( ["main","multiqc","test"], workflows ) :

        # execute process
        multiqc_p1.execute()

        # execute a process with dependencies
        multiqc_p2.depends_on=[multiqc_p1.hash]
        multiqc_p2.execute()

        # wait for all above processes to complete
        jawm.Process.wait(multiqc_p2.hash)

        # print the output
        print(multiqc_p1.get_output())
        print(multiqc_p2.get_output())

        multiqc_submodule.multiqc_submodule_p1.execute()
        template._template_p2.execute()

        jawm.Process.wait([ multiqc_submodule.multiqc_submodule_p1.hash, template._template_p2.hash  ])
        print(multiqc_submodule.multiqc_submodule_p1.get_output())
        print(template._template_p2.get_output())

    if workflow( "test", workflows ) :

        # for the test workflow we also do something more (just for multiqc)
        multiqc_p3.execute()
        jawm.Process.wait( multiqc_p3.hash)
        print("Test completed.")


    sys.exit(0)
