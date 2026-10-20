import jiwer

def wer_cer(reference, hypothesis):
  # Calculate WER
  wer = jiwer.wer(reference, hypothesis)
  #print(f"Word Error Rate (WER): {wer:.4f}")

  # Calculate CER
  cer = jiwer.cer(reference, hypothesis)
  #print(f"Character Error Rate (CER): {cer:.4f}")

  return wer, cer


gt = open("kpti_log_grok.txt",'r',encoding="utf-8",errors='ignore')

cerlist=0
werlist=0
N=2553
for i in range(N):
    line=gt.readline()
    line=line.replace('\t\t\t','\t')
    line=line.replace('\t\t','\t')

    tlines=line.split('\t')
    ref=tlines[1]
    predicted=tlines[2]
    print(ref)
    print(predicted)
    wer, cer= wer_cer(ref, predicted)
    werlist+=wer
    cerlist+=cer

MeanWER=werlist/N
MeanCER=cerlist/N
print("The Mean WER is:"+str(MeanWER))
print("Total Mean CER is :"+str(MeanCER))