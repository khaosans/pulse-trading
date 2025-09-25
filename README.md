# Pulse Trading Marketing Plan Presentation SPA

An interactive Single Page Application (SPA) for presenting the Pulse Trading marketing plan, enhanced with local Ollama AI integration for content improvement and insights generation.

## 🚀 Features

- **Interactive Presentation**: 15-slide professional presentation with smooth transitions
- **AI Enhancement**: Local Ollama integration for content improvement and insights
- **Speaker Notes**: Built-in speaker notes panel for presentation guidance
- **Keyboard Navigation**: Full keyboard support for seamless presentation flow
- **Responsive Design**: Optimized for desktop, tablet, and mobile viewing
- **Professional UI**: Modern, clean design with smooth animations

## 📋 Prerequisites

### Ollama Setup (for AI features)
1. Install Ollama from [ollama.ai](https://ollama.ai)
2. Pull the required model:
   ```bash
   ollama pull llama3.2
   ```
3. Start Ollama service:
   ```bash
   ollama serve
   ```

### Node.js (optional, for development)
- Node.js 16+ recommended
- npm or yarn package manager

## 🛠️ Installation & Setup

### Option 1: Simple HTTP Server (Recommended)
```bash
# Navigate to the project directory
cd "pulse trading"

# Start a simple HTTP server
python -m http.server 8000
# OR
python3 -m http.server 8000
```

### Option 2: Using Node.js
```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

### Option 3: Using npx serve
```bash
npx serve . -p 8000
```

## 🌐 Access the Application

Open your browser and navigate to:
- **Local**: `http://localhost:8000`
- **Network**: `http://[your-ip]:8000` (for remote access)

## 🎮 Usage

### Navigation
- **Mouse**: Click navigation buttons or use arrow buttons
- **Keyboard**: 
  - `Arrow Keys` / `Space`: Navigate slides
  - `F`: Toggle fullscreen
  - `N`: Toggle speaker notes
  - `A`: Toggle AI panel
  - `Escape`: Exit fullscreen
  - `?`: Show keyboard shortcuts help

### AI Features (Requires Ollama)
1. Click the AI panel toggle button (right side)
2. Use the AI enhancement buttons:
   - **Enhance Content**: Improve current slide content
   - **Generate Insights**: Create strategic insights
   - **Improve Narrative**: Enhance storytelling

### Speaker Notes
- Click the speaker notes toggle to show/hide notes
- Notes automatically update based on current slide
- Export notes using the export functionality

## 📁 Project Structure

```
pulse-trading/
├── index.html              # Main HTML file
├── styles.css              # CSS styling
├── script.js               # JavaScript functionality
├── package.json            # Node.js dependencies
├── README.md               # This file
├── Pulse_Trading_Professional_Presentation.md  # Source content
└── [other presentation files]
```

## 🎨 Customization

### Adding New Slides
1. Add slide HTML in `index.html`
2. Update `totalSlides` in `script.js`
3. Add speaker notes in the `speakerNotes` object
4. Update navigation logic if needed

### Styling
- Modify `styles.css` for visual changes
- CSS variables are defined at the top for easy theming
- Responsive breakpoints are included for mobile optimization

### AI Integration
- Modify the Ollama API calls in `script.js`
- Change the model by updating the `model` parameter
- Add new AI features by creating new methods

## 🔧 Technical Details

### Technologies Used
- **HTML5**: Semantic markup and structure
- **CSS3**: Modern styling with Flexbox/Grid
- **Vanilla JavaScript**: No frameworks, pure JS
- **Ollama API**: Local AI model integration
- **Font Awesome**: Icons
- **Google Fonts**: Typography (Inter font family)

### Browser Support
- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

### Performance
- Optimized for smooth 60fps animations
- Lazy loading for better performance
- Minimal dependencies for fast loading

## 🚀 Deployment

### Static Hosting
The application is a static SPA and can be deployed to:
- **GitHub Pages**: Push to repository and enable Pages
- **Netlify**: Drag and drop the folder
- **Vercel**: Connect repository
- **AWS S3**: Upload files to S3 bucket
- **Any web server**: Upload files to web root

### Docker (Optional)
```dockerfile
FROM nginx:alpine
COPY . /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

MIT License - see LICENSE file for details

## 🆘 Troubleshooting

### Ollama Connection Issues
- Ensure Ollama is running: `ollama serve`
- Check if the model is installed: `ollama list`
- Verify API endpoint: `http://localhost:11434/api/tags`

### CORS Issues
- Use a proper HTTP server (not file:// protocol)
- Ensure Ollama allows CORS requests
- Check browser console for error messages

### Performance Issues
- Disable AI features if not needed
- Use a modern browser
- Clear browser cache

## 📞 Support

For issues or questions:
- Create an issue in the GitHub repository
- Contact the development team
- Check the troubleshooting section above

---

**Pulse Trading Team**: Kennedy, Derek, Shang, Maryam, Scott, Sour
