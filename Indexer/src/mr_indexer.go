package main

import (
  "flag"
  "math"
  "strings"
  "time"
  "strconv"
  _ "github.com/chrislusf/glow/driver"
  "github.com/chrislusf/glow/flow"
  "database/sql"
  _ "github.com/go-sql-driver/mysql"
)

// ClassDescription groups the description of a class with its id.
type ClassDescription struct {
  ClassID string 
  Description string 
}

// ClassToken groups a token of a class's description with its id.
type ClassToken struct {
  ClassID string
  Token string
}

// SimilarClasses groups a class's id with a encoded string containing itself
// and a similar class's id.
type SimilarClasses struct {
  ClassID string
  CombinedClassIDs string
}

// ClassIDTermFrequencyPair groups a class's id with one of its token's frequency.
type ClassIDTermFrequencyPair struct {
  ClassID string
  Frequency float64
}

// TermFrequency describes a token's frequency in a doc.
type TermFrequency struct {
  Token string
  ClassIDTermFrequencyPair
}

// Feature represents a token's weight in a doc.
type Feature struct {
  Token string
  Weight float64
}

// ClassIDAndFeatureVector groups a class's id and its feature vector.
type ClassIDAndFeatureVector struct {
  ClassID string
  FeatureVector map[string]float64
}

// ClassIDAndIDF groups a class id and the idf of one of its tokens.
type ClassIDAndIDF struct {
  ClassID string
  Idf float64
}

// Similarity groups a class's id and its score relative to another class
type Similarity struct {
  ClassID string
  Score float64
}

// Similarities is a list of Similarity.
type Similarities []Similarity

// ClassIDSimilarity groups a class's id and its similarity with another class.
type ClassIDSimilarity struct {
  ClassID string
  Similarity
}

// WeightedFeatureVector groups a feature vector with its weight.
type WeightedFeatureVector struct {
  Weight float64
  FeatureVector map[string]float64
}

var documentCount int
var idf_threshold float64

// IsValidToken returns true if the token is valid.
func IsValidToken(token string) bool {
  if len(token) < 3 {
    return false
  }

  return true
}


// ProcessDescriptions reads a tab separated file, processes the descriptions,
// and converts it into a channel of ClassDescriptions.

func ProcessData(out chan ClassDescription, query string) {
  db, err := sql.Open("mysql", "cs130:cs130@/cs130")
  if err != nil {
    panic("ProcessData: Could not read db") 
  }

  classIdAndDataList, err := db.Query(query)

  if err != nil {
    panic("ProcessData: Could not run select query")
  }

  for classIdAndDataList.Next() {
    var id int
    var data string

    err = classIdAndDataList.Scan(&id, &data)

    if err != nil {
      print("ProcessData: Failed to get row")
    }

    id_string := strconv.Itoa(id)
    documentCount++
    out <- ClassDescription{id_string, data}
  }
}

func ProcessDescriptions(out chan ClassDescription) {
  idf_threshold = 20.0
  ProcessData(out, "SELECT id, description FROM filtered_lecture_data")
}

func ProcessTitles(out chan ClassDescription) {
  idf_threshold = 1.0
  ProcessData(out, "SELECT id, title FROM filtered_lecture_data")
}

// TokenizeDescription tokenizes the description of a ClassDescription.
func TokenizeDescription(classDescription ClassDescription, out chan string) {
  tokens := strings.Split(classDescription.Description, " ")
  tokenMap := make(map[string]struct{})

  for _, token := range tokens {
    if !IsValidToken(token) {
      continue
    }

    if _, ok := tokenMap[token]; !ok {
      out <- token
      // hack to use 0 bytes for value
      tokenMap[token] = struct{}{}
    }
  }
}

// SumReducer is a basic SumReducer.
func SumReducer(left int, right int) int {
  return left + right
}

// GenerateIDF Calculates the idf weight for a token.
func GenerateIDF(token string, count int) (string, float64) {
  return token, math.Log10(float64(documentCount) / float64(count))
}

// PreprocessForSumReducer preprocesses the data for the SumReducer.
func PreprocessForSumReducer(token string) (string, int) {
  return token, 1
}

// CalculateTermFrequency calculates the term frequency for all tokens in a description.
func CalculateTermFrequency(classDescription ClassDescription, out chan TermFrequency) {
  ClassID := classDescription.ClassID
  tokens := strings.Split(classDescription.Description, " ")
  tokenCounter := make(map[string]int)
  totalTokenCount := len(tokens)

  for _, token := range tokens {
    if !IsValidToken(token) {
      continue
    }

    if _, ok := tokenCounter[token]; ok {
      tokenCounter[token]++
    } else {
      tokenCounter[token] = 1
    }
  }

  for token, count := range tokenCounter {
    out <- TermFrequency{token, ClassIDTermFrequencyPair{ClassID, float64(count) / float64(totalTokenCount)}}
  }
}

// ReformatTermFrequency reformats TermFrequency to a KV pair.
func ReformatTermFrequency(termFrequency TermFrequency) (string, ClassIDTermFrequencyPair) {
  return termFrequency.Token, termFrequency.ClassIDTermFrequencyPair
}

// GenerateFeature creates a feature vector for a token.
func GenerateFeature(token string, idf float64, ClassIDTermFrequencyPair ClassIDTermFrequencyPair) (string, Feature) {
  return ClassIDTermFrequencyPair.ClassID, Feature{token, idf * ClassIDTermFrequencyPair.Frequency}
}

// L2NormAndMap takes the L2Norm of the feature vector and then reformats the feature list into a map.
func L2NormAndMap(key string, features []Feature) (string, map[string]float64) {
  var total float64

  for _, feature := range features {
    total += math.Pow(feature.Weight, 2.0)
  }

  total = math.Pow(total, 0.5)

  featureVector := make(map[string]float64)

  for _, feature := range features {
    featureVector[feature.Token] = feature.Weight / total
  }

  return key, featureVector
}

// L2Norm takes the L2Norm of the feature vector.
func L2Norm(key string, featureVector map[string]float64) (string, map[string]float64) {
  var total float64

  for _, weight := range featureVector {
    total += math.Pow(weight, 2.0)
  }

  total = math.Pow(total, 0.5)

  for token, _ := range featureVector {
    featureVector[token] /= total
  }

  return key, featureVector
}

// TokenizeDescriptionToClassToken converts a ClassDescription into a channel of ClassTokens.
func TokenizeDescriptionToClassToken(classDescription ClassDescription, out chan ClassToken) {
  ClassID := classDescription.ClassID
  tokens := strings.Split(classDescription.Description, " ")

  for _, token := range tokens {
    if IsValidToken(token) {
      out <- ClassToken{ClassID, token}
    }
  }
}

// RemapClassToken converts a ClassToken to <token, class id>.
func RemapClassToken(classToken ClassToken) (string, string) {
  return classToken.Token, classToken.ClassID
}

// GroupClasses groups classes that share a common low-idf token.
func GroupClasses(token string, ClassIDs []string, out chan string) {
  for _, outerClassID := range ClassIDs {
    for _, innerClassID := range ClassIDs {
      if outerClassID < innerClassID {
        out <- (outerClassID + "|" + innerClassID)
      }
    }
  }
}

// RemapSimilarClasses comverts a string into a KV pair.  The value is meaningless.
func RemapSimilarClasses(similarClasses string) (string, bool) {
  return similarClasses, true
}

// SimilarClassesReducer picks the first low-idf token that two classes share.
func SimilarClassesReducer(left bool, right bool) bool {
  return left
}

// SplitSimilarClasses converts a ClassIDPair into a channel of SimilarClasses.
func SplitSimilarClasses(ClassIDPair string, emptyBool bool, out chan SimilarClasses) {
  ClassIDs := strings.Split(ClassIDPair, "|")
  out <- SimilarClasses{ClassIDs[0], ClassIDPair}
  out <- SimilarClasses{ClassIDs[1], ClassIDPair}
}

// PreprocessSimilarClassesForJoin remaps SimilarClasses into a KV pair.
func PreprocessSimilarClassesForJoin(similarClasses SimilarClasses) (string, string) {
  return similarClasses.ClassID, similarClasses.CombinedClassIDs
}

// JoinClassSimilarityAndFeatureVector maps similarClasses to its feature vector.
func JoinClassSimilarityAndFeatureVector(ClassID string, similarClasses string, featureVector map[string]float64) (string, map[string]float64) {
  return similarClasses, featureVector
}

// ComputeCosineSimilarityHelper computes the cosine similarity between two feature vectors.
func ComputeCosineSimilarityHelper(shortFeatureVector map[string]float64, longFeatureVector map[string]float64) float64 {
  var total float64

  for key, value := range shortFeatureVector {
    if _, hasKey := longFeatureVector[key]; hasKey {
      total += value * longFeatureVector[key]
    }
  }

  return total
}

// ComputeCosineSimilarity orders the shorter feature vector first to feed to ComputeCosineSimilarityHelper accordingly.
func ComputeCosineSimilarity(shortFeatureVector map[string]float64, longFeatureVector map[string]float64) float64 {
  if len(shortFeatureVector) < len(longFeatureVector) {
    return ComputeCosineSimilarityHelper(shortFeatureVector, longFeatureVector)
  }

  return ComputeCosineSimilarityHelper(longFeatureVector, shortFeatureVector)
}

// ComputeSimilarity computes the similarity between two feature vectors.
func ComputeSimilarity(similarClasses string, featureVectors []map[string]float64) (string, float64) {
  if len(featureVectors) < 2 {
    return similarClasses, 0.0
  }

  return similarClasses, ComputeCosineSimilarity(featureVectors[0], featureVectors[1])
}

// ClassTokenToClassTokenIDF joins the class id and idf into a ClassIDAndIDF.
func ClassTokenToClassTokenIDF(token string, ClassID string, idf float64) (string, ClassIDAndIDF) {
  return token, ClassIDAndIDF{ClassID, idf}
}

// FilterLowIDFTokens filters low-idf tokens.
func FilterLowIDFTokens(token string, ClassIDAndIDF ClassIDAndIDF) bool {
  return  ClassIDAndIDF.Idf > math.Log10(idf_threshold)
}

// ReduceToClassToken remaps a ClassIDAndIDF into just the class id.
func ReduceToClassToken(token string, ClassIDAndIDF ClassIDAndIDF) (string, string) {
  return token, ClassIDAndIDF.ClassID
}

// AddReverseSimilarityScores adds similarity scores to a channel.
func AddReverseSimilarityScores(similarClasses string, similarity float64, out chan string) {
  classes := strings.Split(similarClasses, "|")
  out <- classes[0] + "," + classes[1] + "," + strconv.FormatFloat(similarity, 'E', -1, 64)
  out <- classes[1] + "," + classes[0] + "," + strconv.FormatFloat(similarity, 'E', -1, 64)
}

func (s Similarities) Len() int { return len(s) }
func (s Similarities) Less(i, j int) bool { return s[i].Score < s[j].Score }
func (s Similarities) Swap(i, j int) { s[i], s[j] = s[j], s[i]}

func WriteTitleSimilaritiesToDB() {

}

func main() {
  start := time.Now()
  target := flag.String("target", "description", "title/description")
  flag.Parse()

  // Channel of ClassDescription
  var Process func(out chan ClassDescription)
  //var Write func(ClassID string, similarityScores Similarities)

  if *target == "description" {
    Process = ProcessDescriptions
   // Write = WriteDescriptionSimilaritiesToDB
  } else if *target == "title" {
    Process = ProcessTitles
  //  Write = WriteTitleSimilaritiesToDB
  } else {
    panic("Invalid target flag")
  }

  classDescriptions := flow.New().Source(Process, 4)
  // token -> idf
  idf := classDescriptions.
    Map(TokenizeDescription).
    Map(PreprocessForSumReducer).
    Sort(nil).ReduceByKey(SumReducer).
    Map(GenerateIDF)

  // token -> ClassID, weight
  tf := classDescriptions.
    Map(CalculateTermFrequency).
    Map(ReformatTermFrequency)

  // class_id -> [token, weight]
  featureVector := idf.Join(tf).
    Map(GenerateFeature).
    GroupByKey().
    Map(L2NormAndMap)

  // token -> class id
  classTokens := classDescriptions.
    Map(TokenizeDescriptionToClassToken).
    Map(RemapClassToken)

  filteredClassTokens := classTokens.Join(idf).
    Map(ClassTokenToClassTokenIDF).
    Filter(FilterLowIDFTokens).
    Map(ReduceToClassToken)

  // class id -> similar class ids
  similarClasses := filteredClassTokens.
    GroupByKey().
    Map(GroupClasses).
    Map(RemapSimilarClasses).
    ReduceByKey(SimilarClassesReducer).
    Map(SplitSimilarClasses).
    Map(PreprocessSimilarClassesForJoin)

  // class id -> Similarity
  similarClasses.Join(featureVector).
    Map(JoinClassSimilarityAndFeatureVector).
    GroupByKey().
    Map(ComputeSimilarity).
    Map(AddReverseSimilarityScores).
    SaveTextToFile("tmp.txt")

  elapsed := float64(time.Since(start)) / 1E9
  println("Total Execution Time: ", elapsed, " seconds")
}