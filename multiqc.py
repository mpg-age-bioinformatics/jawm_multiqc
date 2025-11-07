import jawm
import os

# Auto-generated from Nextflow by nf_to_jawm.

multiqc=jawm.Process(
    name="multiqc",
    when=True,
    script="""\
mkdir -p {{multiqc_output}}

if [ {{fastqc}} != "" ] ; then fastqc_folder={{fastqc}} ; else fastqc_folder="" ; fi
if [ {{mapping}} != "" ] ; then mapping_folder={{mapping}} ; else mapping_folder="" ; fi
if [ {{featurecounts}} != "" ] ; then featureCounts_folder={{featurecounts}} ; else featureCounts_folder="" ; fi

multiqc ${fastqc_folder} ${mapping_folder} ${featureCounts_folder} -f -o {{multiqc_output}}

""",
    desc={
        "multiqc_output":"",
        "fastqc":"",
        "mapping":"",
        "featurecounts":""
    },
    container="mpgagebioinformatics/multiqc:1.13",
    manager_slurm={ "-c": 2, "--mem": "4GB", "-t": "1h" }
)


if __name__ == "__main__":
    import sys
    from jawm.utils import workflow
    from pathlib import Path

    workflows, var, args, unknown_args = jawm.utils.parse_arguments(['main','multiqc','test'])

    if workflow(["main","multiqc","test"], workflows):

        multiqc.execute()
        jawm.Process.wait()
