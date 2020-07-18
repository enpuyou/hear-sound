# %%
from surfboard.sound import Waveform
# import numpy as np
import pandas as pd
import altair as alt


path = "../resources/no-god.wav"
# Instantiate from a .wav file.
sound = Waveform(path=path, sample_rate=44100)

# OR: instantiate from a numpy array.
# sound = Waveform(signal=np.sin(np.arange(0, 2 * np.pi, 1/24000)), sample_rate=44100)

f0_contour = sound.f0_contour()
# %%
# print(f0_contour)
df = pd.DataFrame(f0_contour[0], columns=["pitch"])
df["temp"] = df.index
print(df)
alt.renderers.enable('mimetype')
alt.Chart(df).mark_line().encode(x="temp", y="pitch")




# %%
