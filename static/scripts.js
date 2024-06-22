// Constants for labels and colors
const HEALTHY_LABEL = "healthy";
const PARASITIZED_LABEL = "parasitized";
const GREEN = "#a4f6a5";
const RED = "#f68787";
const CORRECT = "correct";
const INCORRECT = "incorrect";
const SPINNER = '<i class="c-inline-spinner"></i>';

/**
 * Fetches a random image path and its proper label from the server.
 * @returns {Promise<Object>} A promise that resolves to an object containing the image path and proper label.
 */
async function getRandomImageAndLabel() {
  const response = await fetch("/get-image-path-and-label");
  return await response.json();
}

/**
 * Fetches the prediction for the given image path from the server.
 * @param {string} imagePath - The path of the image to be predicted.
 * @returns {Promise<Object>} A promise that resolves to an object containing prediction information.
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
 * Displays spinner icons in the prediction output elements.
 */
function showPredictionSpinners() {
  document.getElementById("raw-output").innerHTML = SPINNER;
  document.getElementById("healthy-probability").innerHTML = SPINNER;
  document.getElementById("prediction").innerHTML = SPINNER;
  document.getElementById("confidence").innerHTML = SPINNER;
}

/**
 * Displays spinner icons in all relevant elements to indicate loading.
 */
function showAllSpinners() {
  document.getElementById("proper-label").innerHTML = SPINNER;
  showPredictionSpinners();
  document.getElementById("correctness").innerHTML = SPINNER;
}

/**
 * Displays the given image in the designated image element.
 * @param {string} imagePath - The path of the image to be displayed.
 */
function showImage(imagePath) {
  const img = document.getElementById("predict-image");
  img.src = imagePath;
}

/**
 * Displays the prediction results in the corresponding HTML elements.
 * @param {number} rawOutput - The raw output value from the prediction model.
 * @param {number} healthyProbability - The probability that the image is healthy.
 * @param {string} prediction - The predicted label (healthy or parasitized).
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
 * Displays the proper label for the image in the corresponding HTML element.
 * @param {string} label - The proper label (healthy or parasitized) of the image.
 */
function showProperLabel(label) {
  const properLabel = document.getElementById("proper-label");
  properLabel.innerHTML = label;
  properLabel.style.color = label === HEALTHY_LABEL ? GREEN : RED;
}

/**
 * Displays whether the model's prediction was correct or incorrect.
 * @param {string} prediction - The predicted label.
 * @param {string} properLabel - The proper label of the image.
 */
function showModelCorrectness(prediction, properLabel) {
  const correctness = document.getElementById("correctness");
  const isCorrect = prediction === properLabel;
  correctness.style.color = isCorrect ? GREEN : RED;
  correctness.innerHTML = isCorrect ? CORRECT : INCORRECT;
}

/**
 * Handles the process of loading the next image, making predictions, and updating the UI.
 */
async function nextImage() {
  const submitButton = document.getElementById("next-image-button");
  submitButton.disabled = true;

  showAllSpinners(); // Replace old content with spinners

  const imagePathAndLabel = await getRandomImageAndLabel();
  showImage(imagePathAndLabel.filepath);
  showProperLabel(imagePathAndLabel.proper_label);

  const predictionInfo = await getPrediction(imagePathAndLabel.filepath);
  showPredictions(
    predictionInfo.raw_output,
    predictionInfo.healthy_probability,
    predictionInfo.prediction,
    predictionInfo.confidence,
  );
  showModelCorrectness(
    predictionInfo.prediction,
    imagePathAndLabel.proper_label,
  );

  submitButton.disabled = false;
}

/**
 * Handles the process of uploading an image, making predictions, and updating the UI.
 */
async function uploadAndPredict() {
  const files = document.getElementById("file-input").files;

  if (files.length === 0) {
    return;
  }

  showPredictionSpinners(); // Replace old content with spinners

  const imageURL = window.URL.createObjectURL(files[0]);
  showImage(imageURL);

  const data = new FormData();
  data.append("file", files[0]);

  const response = await fetch("/upload-and-predict", {
    method: "POST",
    body: data,
  });
  const result = await response.json();

  showPredictions(
    result.raw_output,
    result.healthy_probability,
    result.prediction,
    result.confidence,
  );
}
