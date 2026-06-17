export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface User {
  id: string;
  email: string;
  display_name: string | null;
  is_premium: boolean;
}

export interface Language {
  id: number;
  code: string;
  name: string;
}

export interface Track {
  id: number;
  language_id: number;
  title: string;
  title_ru: string;
  title_en: string;
  title_kz: string;
  description: string | null;
  description_ru: string | null;
  description_en: string | null;
  description_kz: string | null;
  language: Language | null;
}

export interface LevelMapItem {
  id: number;
  order_num: number;
  title: string;
  title_ru: string;
  title_en: string;
  title_kz: string;
  difficulty_code: string;
  difficulty_name: string;
  difficulty_name_ru: string;
  difficulty_name_en: string;
  difficulty_name_kz: string;
  status: "locked" | "open" | "completed";
}

export interface LevelDetail {
  id: number;
  track_id: number;
  order_num: number;
  title: string;
  title_ru: string;
  title_en: string;
  title_kz: string;
  task_text: string;
  task_text_ru: string;
  task_text_en: string;
  task_text_kz: string;
  starter_code: string;
  status: string;
  allowed_concepts: string[];
  difficulty_code: string;
  difficulty_name: string;
  difficulty_name_ru: string;
  difficulty_name_en: string;
  difficulty_name_kz: string;
  theory?: string;
  theory_ru?: string;
  theory_en?: string;
  theory_kz?: string;
}

export interface RunCodeResult {
  passed: boolean;
  stdout: string;
  stderr: string;
  details: unknown[];
}

export interface ProgressSummary {
  total_levels: number;
  completed_levels: number;
  by_track: Record<string, number>;
}

export interface Exam {
  id: number;
  exam_type: string;
  title: string;
  title_ru: string;
  title_en: string;
  title_kz: string;
  description: string | null;
  description_ru: string | null;
  description_en: string | null;
  description_kz: string | null;
  pass_percent: number;
  time_limit_min: number | null;
  available: boolean;
  passed: boolean;
  best_score: number | null;
  attempts_used: number;
}

export interface ExamQuestion {
  id: number;
  order_num: number;
  task_text: string;
  task_text_ru: string;
  task_text_en: string;
  task_text_kz: string;
  starter_code: string;
}

export interface StartExamResponse {
  attempt_id: number;
  exam_id: number;
  questions: ExamQuestion[];
}

export interface AiHintResponse {
  hint: string;
}

export type Lang = "ru" | "en" | "kz";

/** Helper: pick the correct localized field from an object based on language */
export function pickLang<T extends Record<string, unknown>>(
  obj: T,
  field: string,
  lang: Lang,
  fallback = ""
): string {
  const key = `${field}_${lang}` as keyof T;
  const fallbackKey = `${field}_ru` as keyof T;
  const direct = field as keyof T;
  return (
    (obj[key] as string) ||
    (obj[fallbackKey] as string) ||
    (obj[direct] as string) ||
    fallback
  );
}

// ── Отзывы о курсах ──────────────────────────────────────────────────────────

export interface Review {
  id: number;
  user_id: string;
  display_name: string | null;
  track_id: number;
  rating: number;
  comment: string | null;
  created_at: string;
  updated_at: string | null;
  is_own: boolean;
}

export interface ReviewCreate {
  rating: number;
  comment?: string | null;
}

export interface TrackReviewsData {
  track_id: number;
  average_rating: number | null;
  total_reviews: number;
  reviews: Review[];
  can_review: boolean;
  my_review: Review | null;
}

export interface ExamReview {
  id: number;
  user_id: string;
  display_name: string | null;
  exam_id: number;
  rating: number;
  comment: string | null;
  created_at: string;
  updated_at: string | null;
  is_own: boolean;
}

export interface ExamReviewsData {
  exam_id: number;
  average_rating: number | null;
  total_reviews: number;
  reviews: ExamReview[];
  can_review: boolean;
  my_review: ExamReview | null;
}

export interface TrackReviewSummary {
  track_id: number;
  track_title: string;
  average_rating: number | null;
  total_reviews: number;
  reviews: Review[];
}

export interface ExamReviewSummary {
  exam_id: number;
  exam_title: string;
  exam_type: string;
  average_rating: number | null;
  total_reviews: number;
  reviews: ExamReview[];
}

export interface AllReviewsData {
  tracks: TrackReviewSummary[];
  exams: ExamReviewSummary[];
  total_reviews: number;
}

