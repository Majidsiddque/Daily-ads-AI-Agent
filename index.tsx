import { registerRoot, Composition } from "remotion";
import { AdComposition } from "./AdComposition";
import config from "../../output/remotion_config.json";

const Root = () => (
  <Composition
    id="AdComposition"
    component={AdComposition}
    durationInFrames={config.durationInFrames ?? 1800}
    fps={config.fps ?? 30}
    width={1080}
    height={1920}
    defaultProps={{
      scenes: config.scenes ?? [],
      voiceover_path: config.voiceover_path ?? "",
    }}
  />
);

registerRoot(Root);
