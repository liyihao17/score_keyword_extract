import Reader
import Segmentation
import Candidate

def PrintExtractedResult(extracted_result):
    print("extracted key words result is")
    for i in range(len(extracted_result)):
        print(extracted_result[i])
    print("there is total " + str(i) + " key words")

def PrintExtractedWord(extracted_word):
    print("extracted key words is")
    for i in range(len(extracted_word)):
        print(extracted_word[i])


def main():
    result = Reader.readfile('result0.bin')
    result_split = Segmentation.SplitCluster(result)
    delete_result = Candidate.DeleteRepetition(result_split)
    candidate = Candidate.BuildClass(delete_result)
    Candidate.CalLenScore(candidate,2,15)
    Candidate.CalSupScore(candidate,result_split)
    Candidate.CalPosScore(candidate,result_split)
    for i in range(len(candidate)):
        for j in range(len(candidate[i])):
            candidate[i][j].CalScore()
    candidate_list = Candidate.GenCandidateList(candidate)
    sorted_candidate_list = Candidate.CandidateListSort(candidate_list)

    extracted_word = Candidate.CutByRank(sorted_candidate_list,0.5)
    PrintExtractedWord(extracted_word)

    # extracted_word = Candidate.CutByScore(sorted_candidate_list,2.5)
    # PrintExtractedWord(extracted_word)

    extracted_word = Candidate.CutByRankAndScore(sorted_candidate_list,0.05,2.9)
    PrintExtractedWord(extracted_word)

    extracted_result = Candidate.ExtractedWordDeleteRepetition(extracted_word)
    PrintExtractedResult(extracted_result)



    # print("")
    # print("")
    # print("")
    # print("")
    #
    # extracted_word = Candidate.CutByScore(sorted_candidate_list,2.0)
    # print("the result of cut by score: ")
    # for i in range(len(extracted_word)):
    #     print("")
    #     for j in range(len(extracted_word[i])):
    #         print(extracted_word[i][j])

if __name__ == "__main__":
    main()