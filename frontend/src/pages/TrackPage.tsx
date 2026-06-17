import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { ArrowLeft, Loader2 } from "lucide-react";
import { api } from "../api/client";
import type { LevelMapItem, Track } from "../api/types";
import { LevelMap } from "../components/LevelMap";
import { ReviewsSection } from "../components/ReviewsSection";

export function TrackPage() {
  const { trackId } = useParams<{ trackId: string }>();
  const id = Number(trackId);
  const [track, setTrack] = useState<Track | null>(null);
  const [levels, setLevels] = useState<LevelMapItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) return;
    Promise.all([
      api.get<Track[]>("/tracks").then((list) => list.find((t) => t.id === id) ?? null),
      api.get<LevelMapItem[]>(`/levels/track/${id}/map`),
    ])
      .then(([t, l]) => {
        setTrack(t);
        setLevels(l);
      })
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) {
    return (
      <div className="flex justify-center py-20">
        <Loader2 className="w-10 h-10 animate-spin text-academy-accent" />
      </div>
    );
  }

  return (
    <div>
      <Link
        to="/"
        className="inline-flex items-center gap-1 text-sm text-academy-muted hover:text-white mb-4"
      >
        <ArrowLeft className="w-4 h-4" />
        Все треки
      </Link>
      <h1 className="text-2xl font-bold mb-1">{track?.language?.name ?? "Трек"}</h1>
      <p className="text-academy-muted mb-8">Карта уровней — выберите доступный этап</p>
      <LevelMap trackId={id} levels={levels} />

      {/* Divider */}
      <div className="border-t border-academy-border/40 mt-10" />

      {/* Reviews section */}
      <ReviewsSection trackId={id} />
    </div>
  );
}

