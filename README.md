<p align="center">
  <img src="/doc/no-bg-banner.png" alt="No Backdrop - AI Background Removal" width="100%"/>
</p>

#### [Demo](https://no.hossain.cc/) &nbsp; · &nbsp; [Report a bug](https://github.com/kazisean/no-backdrop/issues/new) &nbsp; · &nbsp; [Installation](#Installation)

# No Backdrop
> Remove background from images within seconds powered by AI. Process thousands of images with speed, accuracy, and reliability.

[![Built with Next.js](https://img.shields.io/badge/Built%20with-Next.js-000000?style=flat-square&logo=Next.js&logoColor=white)](https://nextjs.org) [![API: FastAPI](https://img.shields.io/badge/API-FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com) [![Model: u2net](https://img.shields.io/badge/Model-u2net-blue?style=flat-square)](https://github.com/xuebinqin/U-2-Net) [![Uptime: 99.9%](https://img.shields.io/badge/Uptime-99.9%25-brightgreen?style=flat-square)](https://no-backdrop.yourdomain.com/status)


### Key Features

- **Instant Background Removal**: Remove backgrounds in seconds.
- **Batch Processing**: Handle multiple images simultaneously.
- **High Throughput**: Process thousands of images without performance degradation
- **Libre Pricing**: Free for now! Feel free to self-host it!

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/no-backdrop.git
cd no-backdrop

# Install dependencies
npm install

# Run the development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to see the application.

## Tech Stack

- [Next.js](https://nextjs.org/) - Frontend
- [FastAPI](https://fastapi.tiangolo.com/) - Backend API
- [Rembg Library](https://github.com/danielgatis/rembg) - Backend library to remove image background
- [u2net](https://github.com/xuebinqin/U-2-Net) - State-of-the-art deep learning model for salient object detection
- [Vercel](https://vercel.com/) - Frontend hosting and serverless functions
- [CloudFuntion](https://cloud.google.com/functions) - For backend hosting

## License

MIT