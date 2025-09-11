# Gemini Image Analysis Tool

A simplified Python tool for analyzing images with Google's Gemini 2.5 Flash Lite model using system prompts and JSON output.

## Features

- 🖼️ **Image Analysis**: Analyze images with custom system prompts
- 📄 **JSON Output**: Get structured JSON responses from the model
- ⚙️ **System Prompt**: Configure custom prompts for consistent analysis
- 🔧 **Simple Usage**: Single command to analyze any image

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the API key

### 3. Configure Environment

1. Edit `config.env` and add your API key:
```env
GEMINI_API_KEY=your_actual_api_key_here
```

2. Optionally customize the system prompt:
```env
SYSTEM_PROMPT=Your custom prompt for image analysis...
```

## Usage

### Basic Usage

```bash
# Analyze an image
python gemini_explorer.py image.jpg

# Analyze an image and save to specific JSON file
python gemini_explorer.py image.jpg my_analysis.json
```

### Supported Image Formats

- JPG/JPEG
- PNG
- GIF
- BMP
- WebP

## Configuration

### System Prompt

The system prompt is sent to the model with every image. You can customize it in `config.env`:

```env
SYSTEM_PROMPT=Analyze this image and provide a detailed JSON response with your observations. Include information about objects, colors, composition, and any other relevant details in a structured JSON format.
```

### Example System Prompts

**For Object Detection:**
```env
SYSTEM_PROMPT=Identify all objects in this image and return a JSON array with object names, positions, and confidence levels.
```

**For Color Analysis:**
```env
SYSTEM_PROMPT=Analyze the color palette of this image and return a JSON object with dominant colors, color harmony, and mood.
```

**For Scene Description:**
```env
SYSTEM_PROMPT=Describe this scene in detail and return a JSON object with location, time of day, weather, and activities.
```

## Output

The tool outputs:
1. **Console**: Shows the analysis result
2. **JSON File**: Saves the result to a JSON file (default: `analysis_output.json`)

If the model output is not valid JSON, it will be wrapped in a JSON structure:
```json
{
  "raw_output": "model response here",
  "note": "Output was not valid JSON, saved as raw text"
}
```

## Examples

```bash
# Analyze a photo
python gemini_explorer.py photo.jpg

# Analyze with custom output file
python gemini_explorer.py screenshot.png detailed_analysis.json
```

## File Structure

```
├── gemini_explorer.py    # Main script
├── requirements.txt      # Python dependencies
├── config.env           # Configuration file
└── README.md            # This file
```

## Troubleshooting

### Common Issues

1. **API Key Error**: Make sure your `GEMINI_API_KEY` is correctly set in `config.env`
2. **Module Not Found**: Run `pip install -r requirements.txt`
3. **Image Not Found**: Check the image path is correct
4. **Unsupported Format**: Use supported image formats (JPG, PNG, GIF, BMP, WebP)

## License

This project is for educational and exploration purposes. Please review Google's terms of service for the Gemini API.