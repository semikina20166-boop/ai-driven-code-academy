import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import { I18nProvider } from "./i18n/I18nContext";
import { Layout } from "./components/Layout";
import { ProtectedRoute } from "./components/ProtectedRoute";
import { DashboardPage } from "./pages/DashboardPage";
import { ExamSessionPage } from "./pages/ExamSessionPage";
import { ExamsPage } from "./pages/ExamsPage";
import { LevelPage } from "./pages/LevelPage";
import { LoginPage } from "./pages/LoginPage";
import { RegisterPage } from "./pages/RegisterPage";
import { TrackPage } from "./pages/TrackPage";
import { ProfilePage } from "./pages/ProfilePage";
import { BillingPage } from "./pages/BillingPage";
import { LecturesPage } from "./pages/LecturesPage";

export default function App() {
  return (
    <BrowserRouter>
      <I18nProvider>
        <AuthProvider>
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route element={<ProtectedRoute />}>
              <Route element={<Layout />}>
                <Route index element={<DashboardPage />} />
                <Route path="tracks/:trackId" element={<TrackPage />} />
                <Route path="tracks/:trackId/levels/:levelId" element={<LevelPage />} />
                <Route path="exams" element={<ExamsPage />} />
                <Route path="exams/:examId/session" element={<ExamSessionPage />} />
                <Route path="profile" element={<ProfilePage />} />
                <Route path="billing" element={<BillingPage />} />
                <Route path="lectures" element={<LecturesPage />} />
              </Route>
            </Route>
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </AuthProvider>
      </I18nProvider>
    </BrowserRouter>
  );
}
