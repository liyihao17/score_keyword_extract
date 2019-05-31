import Reader
import Segmentation
import Candidate

def main():
    result = Reader.readfile('result38.bin')
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

    extracted_word = Candidate.CutByRank(sorted_candidate_list,0.15)
    print("the result of cut by rank: ")
    for i in range(len(extracted_word)):
        print("")
        for j in range(len(extracted_word[i])):
            print(extracted_word[i][j])

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