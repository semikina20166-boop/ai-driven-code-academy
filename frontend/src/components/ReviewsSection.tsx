import { useEffect, useState } from "react";
import { Star, MessageSquarePlus, Edit3, ChevronDown, ChevronUp, Loader2 } from "lucide-react";
import { api } from "../api/client";
import type { TrackReviewsData, Review, ReviewCreate } from "../api/types";

interface Props {
  trackId: number;
}

function StarRating({
  value,
  onChange,
  readonly = false,
  size = "md",
}: {
  value: number;
  onChange?: (v: number) => void;
  readonly?: boolean;
  size?: "sm" | "md" | "lg";
}) {
  const [hovered, setHovered] = useState(0);
  const dim = size === "lg" ? "w-8 h-8" : size === "md" ? "w-6 h-6" : "w-4 h-4";
  const active = hovered || value;

  return (
    <div className="flex gap-0.5">
      {[1, 2, 3, 4, 5].map((n) => (
        <button
          key={n}
          type="button"
          disabled={readonly}
          onClick={() => onChange?.(n)}
          onMouseEnter={() => !readonly && setHovered(n)}
          onMouseLeave={() => !readonly && setHovered(0)}
          className={`transition-all duration-150 ${readonly ? "cursor-default" : "cursor-pointer hover:scale-110"}`}
          aria-label={`Оценка ${n}`}
        >
          <Star
            className={`${dim} transition-colors duration-150 ${
              n <= active
                ? "fill-amber-400 text-amber-400"
                : "fill-transparent text-slate-600"
            }`}
          />
        </button>
      ))}
    </div>
  );
}

function AverageStars({ avg, total }: { avg: number | null; total: number }) {
  if (avg === null || total === 0) return null;
  const full = Math.floor(avg);
  const partial = avg - full;

  return (
    <div className="flex items-center gap-3">
      <span className="text-4xl font-bold text-white">{avg.toFixed(1)}</span>
      <div>
        <div className="flex gap-0.5 mb-1">
          {[1, 2, 3, 4, 5].map((n) => {
            const fill =
              n <= full
                ? 1
                : n === full + 1 && partial > 0
                ? partial
                : 0;
            return (
              <div key={n} className="relative w-5 h-5">
                <Star className="absolute w-5 h-5 fill-transparent text-slate-600" />
                <div
                  className="absolute overflow-hidden h-full"
                  style={{ width: `${fill * 100}%` }}
                >
                  <Star className="w-5 h-5 fill-amber-400 text-amber-400" />
                </div>
              </div>
            );
          })}
        </div>
        <p className="text-xs text-slate-400">
          {total} {total === 1 ? "отзыв" : total < 5 ? "отзыва" : "отзывов"}
        </p>
      </div>
    </div>
  );
}

function ReviewCard({ review }: { review: Review }) {
  const [expanded, setExpanded] = useState(false);
  const initials = (review.display_name || review.user_id.slice(0, 2))
    .toUpperCase()
    .slice(0, 2);
  const date = new Date(review.created_at).toLocaleDateString("ru-RU", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });
  const isLong = (review.comment?.length ?? 0) > 200;
  const displayComment =
    isLong && !expanded
      ? review.comment!.slice(0, 200) + "…"
      : review.comment;

  return (
    <div
      className={`relative rounded-xl border p-4 transition-all duration-200 ${
        review.is_own
          ? "border-academy-accent/40 bg-academy-accent/5"
          : "border-academy-border bg-academy-panel/50"
      }`}
    >
      {review.is_own && (
        <span className="absolute top-3 right-3 text-xs font-semibold text-academy-accent bg-academy-accent/10 px-2 py-0.5 rounded-full">
          Ваш отзыв
        </span>
      )}

      <div className="flex items-center gap-3 mb-3">
        {/* Avatar */}
        <div className="w-9 h-9 rounded-full bg-gradient-to-br from-academy-accent to-blue-700 flex items-center justify-center text-sm font-bold text-white shrink-0">
          {initials}
        </div>
        <div>
          <p className="font-semibold text-sm text-white leading-tight">
            {review.display_name || "Пользователь"}
          </p>
          <p className="text-xs text-slate-500">{date}</p>
        </div>
      </div>

      <StarRating value={review.rating} readonly size="sm" />

      {review.comment && (
        <div className="mt-2">
          <p className="text-sm text-slate-300 leading-relaxed whitespace-pre-wrap">
            {displayComment}
          </p>
          {isLong && (
            <button
              type="button"
              onClick={() => setExpanded((e) => !e)}
              className="mt-1 flex items-center gap-1 text-xs text-academy-accent hover:underline"
            >
              {expanded ? (
                <>
                  <ChevronUp className="w-3 h-3" /> Свернуть
                </>
              ) : (
                <>
                  <ChevronDown className="w-3 h-3" /> Читать полностью
                </>
              )}
            </button>
          )}
        </div>
      )}
    </div>
  );
}

function ReviewForm({
  existing,
  trackId,
  onSaved,
}: {
  existing: Review | null;
  trackId: number;
  onSaved: (r: Review) => void;
}) {
  const [rating, setRating] = useState(existing?.rating ?? 0);
  const [comment, setComment] = useState(existing?.comment ?? "");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [open, setOpen] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (rating === 0) {
      setError("Выберите оценку от 1 до 5 звёзд");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const body: ReviewCreate = { rating, comment: comment.trim() || null };
      const saved = await api.post<Review>(`/reviews/track/${trackId}`, body);
      onSaved(saved);
      setOpen(false);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Ошибка сохранения");
    } finally {
      setLoading(false);
    }
  }

  if (!open) {
    return (
      <button
        id="btn-write-review"
        type="button"
        onClick={() => setOpen(true)}
        className="flex items-center gap-2 px-4 py-2.5 rounded-xl border border-academy-accent/40 bg-academy-accent/10 hover:bg-academy-accent/20 text-academy-accent font-medium text-sm transition-all duration-200 hover:scale-[1.02]"
      >
        {existing ? (
          <>
            <Edit3 className="w-4 h-4" /> Редактировать отзыв
          </>
        ) : (
          <>
            <MessageSquarePlus className="w-4 h-4" /> Написать отзыв
          </>
        )}
      </button>
    );
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="rounded-xl border border-academy-accent/30 bg-academy-panel/60 backdrop-blur p-5 space-y-4"
    >
      <h3 className="font-semibold text-white text-sm">
        {existing ? "Редактировать отзыв" : "Оставить отзыв о курсе"}
      </h3>

      <div>
        <label className="block text-xs text-slate-400 mb-1.5">Оценка *</label>
        <StarRating value={rating} onChange={setRating} size="lg" />
      </div>

      <div>
        <label className="block text-xs text-slate-400 mb-1.5">
          Ваши впечатления{" "}
          <span className="text-slate-600">(необязательно)</span>
        </label>
        <textarea
          id="review-comment"
          value={comment}
          onChange={(e) => setComment(e.target.value)}
          rows={4}
          maxLength={2000}
          placeholder="Что понравилось? Что стоит улучшить? Поделитесь рекомендациями для других студентов…"
          className="w-full rounded-lg border border-academy-border bg-academy-bg px-3 py-2 text-sm text-white placeholder-slate-600 focus:outline-none focus:border-academy-accent/60 resize-none"
        />
        <p className="text-right text-xs text-slate-600 mt-0.5">
          {comment.length}/2000
        </p>
      </div>

      {error && (
        <p className="text-rose-400 text-xs font-medium">{error}</p>
      )}

      <div className="flex gap-2">
        <button
          id="btn-submit-review"
          type="submit"
          disabled={loading}
          className="flex items-center gap-2 px-4 py-2 rounded-lg bg-academy-accent hover:bg-blue-600 text-white text-sm font-medium transition-colors disabled:opacity-50"
        >
          {loading && <Loader2 className="w-4 h-4 animate-spin" />}
          Сохранить отзыв
        </button>
        <button
          type="button"
          onClick={() => setOpen(false)}
          className="px-4 py-2 rounded-lg border border-academy-border text-sm text-slate-400 hover:text-white transition-colors"
        >
          Отмена
        </button>
      </div>
    </form>
  );
}

export function ReviewsSection({ trackId }: Props) {
  const [data, setData] = useState<TrackReviewsData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .get<TrackReviewsData>(`/reviews/track/${trackId}`)
      .then(setData)
      .catch(() => setData(null))
      .finally(() => setLoading(false));
  }, [trackId]);

  function handleReviewSaved(saved: Review) {
    setData((prev) => {
      if (!prev) return prev;
      const exists = prev.reviews.some((r) => r.id === saved.id);
      const reviews = exists
        ? prev.reviews.map((r) => (r.id === saved.id ? saved : r))
        : [saved, ...prev.reviews];
      const avg =
        reviews.reduce((s, r) => s + r.rating, 0) / reviews.length;
      return {
        ...prev,
        reviews,
        my_review: saved,
        average_rating: Math.round(avg * 100) / 100,
        total_reviews: reviews.length,
      };
    });
  }

  if (loading) {
    return (
      <div className="flex justify-center py-8">
        <Loader2 className="w-6 h-6 animate-spin text-academy-accent" />
      </div>
    );
  }

  if (!data) return null;

  return (
    <section id="reviews-section" className="mt-10">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
        <div>
          <h2 className="text-lg font-bold text-white mb-1">
            Отзывы о курсе
          </h2>
          {data.average_rating !== null ? (
            <AverageStars avg={data.average_rating} total={data.total_reviews} />
          ) : (
            <p className="text-sm text-slate-500">Отзывов пока нет</p>
          )}
        </div>

        {/* Show form button only for users who completed all levels */}
        {data.can_review && (
          <ReviewForm
            existing={data.my_review}
            trackId={trackId}
            onSaved={handleReviewSaved}
          />
        )}
      </div>

      {/* Hint for users who haven't completed the course */}
      {!data.can_review && (
        <p className="text-xs text-slate-500 mb-4 flex items-center gap-1.5">
          <Star className="w-3.5 h-3.5 text-slate-600" />
          Оставить отзыв можно после прохождения всех уровней курса
        </p>
      )}

      {/* Reviews list */}
      {data.reviews.length > 0 ? (
        <div className="space-y-3">
          {data.reviews.map((r) => (
            <ReviewCard key={r.id} review={r} />
          ))}
        </div>
      ) : (
        <div className="rounded-xl border border-dashed border-academy-border/60 py-10 text-center">
          <Star className="w-10 h-10 text-slate-700 mx-auto mb-3" />
          <p className="text-slate-500 text-sm">Будьте первым, кто оставит отзыв!</p>
        </div>
      )}
    </section>
  );
}
