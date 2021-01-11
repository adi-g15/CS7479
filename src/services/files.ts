const files = [
  {
    name:
      "Lecture 0 [CourseOverview,CourseOutcomes,Syllabus,UnitOutcomes,Books].pdf",
    size: 314,
  },
  {
    name:
      "Lecture 01 [Unit I -  Intro_MicroArchVsArch_Struc_FuncView_NumberSysRep].pdf",
    size: 777,
  },
  {
    name:
      "Lecture 02 [Unit I - IntegerArith-rangeExt,negate,add,sub_ALUdatapath-add,sub].pdf",
    size: 706,
  },
  {
    name:
      "Lecture 03 -Unit I - IntegerArith-UnsignedSignedMul;ALUdatapath-Umul,Smul-.pdf",
    size: 723,
  },
  {
    name: "Lecture 04 -Unit I - IntegerArith-unsigndiv;ALUdatapath-Udiv-.pdf",
    size: 589,
  },
  {
    name:
      "Lecture 05 -Unit I - IntegerArith-signdiv;ALUdatapath-Sdiv;MIPScasestudy-.pdf",
    size: 863,
  },
  {
    name: "Lecture 06 -Unit I - FixedPt,FloatingPtRepresentations-.pdf",
    size: 671,
  },
  {
    name: "Lecture 07 -Unit I - FPArith-add,sub;FPUhardware-add,sub-.pdf",
    size: 654,
  },
  {
    name:
      "Lecture 08 -Unit I - Guard,round,sticky;FPArith-mul,div;FPUhardware-mul,div-.pdf",
    size: 772,
  },
  {
    name: "Lecture 09 [Unit I - CUdesign-Hardwired,Microprogrammed].pdf",
    size: 795,
  },
  {
    name:
      "Lecture 10 [Unit I - CUdesign-Microprogrammed(contd),MicroInsSquncng].pdf",
    size: 682,
  },
  {
    name:
      "Lecture 11 [Unit II - InsSet_CISCvsRISC_InsCycle_InsSetDesign-InsType].pdf",
    size: 1744,
  },
];

export function GetListService(storageRef: firebase.storage.Reference) {
    return new Promise((resolve, reject) => {
        try{
            storageRef.root.listAll().then(result => {
                return resolve(result.items.map(item => {
                    return({
                        name: item.name,
                        link: item.getDownloadURL()
                    });
                }));
            });
        } catch {
            return reject();
        }
    })
  // future -> Use node fs module to get list
}
