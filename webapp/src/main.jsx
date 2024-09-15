import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import {
  createBrowserRouter,
  RouterProvider
} from 'react-router-dom'

// local
import './index.css'

// routes
import HomePage from './routes/home.jsx'
import LoginPage from './routes/login.jsx'
import Dashboard from './routes/dashboard.jsx'
import Repository from './routes/repository.jsx'
import RegisterPage from './routes/register.jsx'

// router
const router = createBrowserRouter([
  {
    path: "/",
    element: <HomePage />
  },
  {
    path: "/login",
    element: <LoginPage />
  },
  {
    path: "/register",
    element: <RegisterPage />
  },
  {
    path: "/dashboard",
    element: <Dashboard />
  },
  {
    path: "/repository/:repositoryId",
    element: <Repository />
  }
])

// main
createRoot(document.getElementById('root')).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
)
