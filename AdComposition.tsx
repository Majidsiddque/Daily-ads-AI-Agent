import { AbsoluteFill, Audio, Img, interpolate, useCurrentFrame, useVideoConfig } from "remotion";

export type Scene = {
  start_ms: number;
  end_ms: number;
  subtitle_text: string;
  image_url: string;
};

type Props = {
  scenes: Scene[];
  voiceover_path: string;
};

const Subtitle: React.FC<{ text: string }> = ({ text }) => (
  <div
    style={{
      position: "absolute",
      bottom: 80,
      left: 0,
      right: 0,
      textAlign: "center",
      fontSize: 38,
      fontWeight: "bold",
      color: "#fff",
      textShadow: "2px 2px 8px #000",
      padding: "0 40px",
    }}
  >
    {text}
  </div>
);

export const AdComposition: React.FC<Props> = ({ scenes, voiceover_path }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const currentMs = (frame / fps) * 1000;

  const activeScene = scenes.find(
    (s) => currentMs >= s.start_ms && currentMs < s.end_ms
  ) ?? scenes[0];

  const opacity = interpolate(frame, [0, 10], [0, 1], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ background: "#000" }}>
      {activeScene?.image_url && (
        <Img
          src={activeScene.image_url}
          style={{ width: "100%", height: "100%", objectFit: "cover", opacity }}
        />
      )}
      <Audio src={voiceover_path} />
      {activeScene && <Subtitle text={activeScene.subtitle_text} />}
    </AbsoluteFill>
  );
};
