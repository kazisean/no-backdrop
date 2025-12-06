<p align="center">
  <a href="https://no.hossain.cc/" target="_blank">
    <img src="/doc/no-bg-banner.png" alt="No Backdrop - AI Background Removal" width="100%"/>
  </a>
</p>

#### [Report a bug](https://github.com/kazisean/no-backdrop/issues/new) &nbsp; · &nbsp; [Installation](#Installation)

# No Backdrop
> Remove background from images within seconds powered by AI. Process thousands of images with speed, accuracy, and reliability.

[![Built with Next.js](https://img.shields.io/badge/Built%20with-Next.js-000000?style=flat-square&logo=Next.js&logoColor=white)](https://nextjs.org) [![API: FastAPI](https://img.shields.io/badge/API-FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com) [![Model: u2net](https://img.shields.io/badge/Model-u2net-blue?style=flat-square)](https://github.com/xuebinqin/U-2-Net) 

### Installation

```bash
# Clone the repository
git clone https://github.com/kazisean/no-backdrop.git
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
- [AWS EC2](https://docs.aws.amazon.com/ec2/) - For backend hosting
- [Celery](https://docs.celeryq.dev/en/stable/) - Asynchronous task queue/job queue
- [Redis](https://redis.io/docs/latest/) - In-memory data store used as a message broker

## Contributing
We welcome contributions from the open-source community. Whether it is a typo or an implementation mistake, your contribution is valuable to us. Please follow these steps:

1. Create an issue describing the problem or enhancement
2. Wait for the issue to be assigned to you 
3. Fork the repository and create a branch for your changes
4. Make your changes and submit a pull request
5. Reference the original issue in your pull request
6. No contribution is too small - we appreciate everything from documentation improvements to major feature additions!

## License

MIT
