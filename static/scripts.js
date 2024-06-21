// Constants
const HEALTHY_LABEL = "healthy";
const PARASITIZED_LABEL = "parasitized";
const GREEN = "#a4f6a5";
const RED = "#f68787";
const CORRECT = "correct";
const INCORRECT = "incorrect";

/**
 * Fetches a random image path and its corresponding label from the server.
 * @returns {Promise<object>} An object containing the image path and label.
 */
async function getRandomImageAndLabel() {
  const response = await fetch("/get-image-path-and-label");
  return await response.json();
}

/**
 * Fetches the prediction for a given image from the server.
 * @param {string} imagePath - The path of the image to be predicted.
 * @returns {Promise<object>} An object containing the prediction results.
 */
async function getPrediction(imagePath) {
  const data = new FormData();
  data.append("filepath", imagePath);

  const response = await fetch("/predict", {
    method: "POST",
    body: data,
  });
  return await response.json();
}

/**
 * Uploads an image file from an input element to the server.
 * @returns {Promise<object|boolean>} The server response containing the image data or false if no files were selected.
 */
async function uploadImage() {
  const files = document.getElementById("file-input").files;

  if (files.length === 0) {
    return false;
  }

  const data = new FormData();
  data.append("file", files[0]);

  const response = await fetch("/upload", {
    method: "POST",
    body: data,
  });
  return await response.json();
}

/**
 * Displays an image on the webpage.
 * @param {string} imagePath - The path of the image to be displayed.
 */
function showImage(imagePath) {
  const img = document.getElementById("predict-image");
  img.src = imagePath;
}

/**
 * Displays the prediction results on the webpage.
 * @param {number} rawOutput - The raw output from the prediction model.
 * @param {number} healthyProbability - The probability that the image is healthy.
 * @param {string} prediction - The prediction label.
 * @param {number} confidence - The confidence level of the prediction.
 */
function showPredictions(
  rawOutput,
  healthyProbability,
  prediction,
  confidence,
) {
  document.getElementById("raw-output").innerHTML = rawOutput.toFixed(4);
  document.getElementById("healthy-probability").innerHTML =
    (healthyProbability * 100).toFixed(2) + "%";
  const predictionLabel = document.getElementById("prediction");
  predictionLabel.innerHTML = prediction;
  predictionLabel.style.color = prediction === HEALTHY_LABEL ? GREEN : RED;
  document.getElementById("confidence").innerHTML =
    (confidence * 100).toFixed(2) + "%";
}

/**
 * Displays the proper label for the image on the webpage.
 * @param {string} label - The correct label for the image.
 */
function showProperLabel(label) {
  const properLabel = document.getElementById("proper-label");
  properLabel.innerHTML = label;
  properLabel.style.color = label === HEALTHY_LABEL ? GREEN : RED;
}

/**
 * Displays whether the model's prediction is correct or incorrect.
 * @param {string} prediction - The model's prediction.
 * @param {string} properLabel - The correct label for the image.
 */
function showModelCorrectness(prediction, properLabel) {
  const correctness = document.getElementById("correctness");
  const isCorrect = prediction === properLabel;
  correctness.style.color = isCorrect ? GREEN : RED;
  correctness.innerHTML = isCorrect ? CORRECT : INCORRECT;
}

/**
 * Fetches and displays a new image and its prediction results.
 */
async function nextImage() {
  const submitButton = document.getElementById("next-image-button");
  submitButton.disabled = true;

  const imagePathAndLabel = await getRandomImageAndLabel();
  showImage(imagePathAndLabel["filepath"]);
  showProperLabel(imagePathAndLabel["proper_label"]);

  const predictionInfo = await getPrediction(imagePathAndLabel["filepath"]);
  showPredictions(
    predictionInfo["raw_output"],
    predictionInfo["healthy_probability"],
    predictionInfo["prediction"],
    predictionInfo["confidence"],
  );
  showModelCorrectness(
    predictionInfo["prediction"],
    imagePathAndLabel["proper_label"],
  );

  submitButton.disabled = false;
}

/**
 * Uploads an image and displays its prediction results.
 */
async function uploadAndPredict() {
  const imageData = await uploadImage();

  if (imageData === false) {
    return;
  }

  showImage(imageData["filepath"]);

  const predictionInfo = await getPrediction(imageData["filepath"]);
  showPredictions(
    predictionInfo["raw_output"],
    predictionInfo["healthy_probability"],
    predictionInfo["prediction"],
    predictionInfo["confidence"],
  );
}
