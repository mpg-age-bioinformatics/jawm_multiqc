import jawm
import os
from pathlib import Path


multiqc=jawm.Process(
    name="multiqc",
    when=lambda p: not os.path.isfile( os.path.join( p.var["multiqc_output"] , "multiqc_report.html" ) ) ,
    script="""\
mkdir -p {{multiqc_output}}

if [ "{{fastqc}}" != "" ] ; then fastqc_folder={{fastqc}} ; else fastqc_folder="" ; fi
if [ "{{mapping}}" != "" ] ; then mapping_folder={{mapping}} ; else mapping_folder="" ; fi
if [ "{{featurecounts}}" != "" ] ; then featureCounts_folder={{featurecounts}} ; else featureCounts_folder="" ; fi

multiqc ${fastqc_folder} ${mapping_folder} ${featureCounts_folder} -f -o {{multiqc_output}}

""",
    desc={
        "multiqc_output":"",
        "fastqc":"",
        "mapping":"",
        "featurecounts":""
    },
    container="mpgagebioinformatics/multiqc:1.13",
    manager_slurm={ "-c": 2, "--mem": "4GB", "-t": "1:00:00" }
)


def report_files(multiqc_output) :
    report_paths={}
    dic={ 
        multiqc_output : { 
            "multiqc":"multiqc_report.html",
            }
        }

    for path in dic :
        directory = Path( path )
        for folder in dic[path] :
            files=[ f.resolve() for f in directory.glob( dic[path][folder] ) ]
            if files :
                report_paths[folder]=files

    return report_paths


if __name__ == "__main__":
    import sys
    from jawm.utils import workflow

    workflows, var, args, unknown_args = jawm.utils.parse_arguments(['main','multiqc','test'])

    if workflow(["main","multiqc","test"], workflows):

        multiqc.execute()
        jawm.Process.wait()
