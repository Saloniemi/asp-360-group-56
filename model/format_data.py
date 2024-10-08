import numpy as np
import pandas as pd

def read_data_np(segment_length):
    df = pd.read_csv('./data_processing/segmented_data_' + str(segment_length) + 's.csv', header=None, skiprows = 1)
    data = []

    for i in range(len(df)):
        data.append([float(value) for value in df.iloc[i].tolist()[1:]])

    # Convert to numpy array
    return np.array(data)



class DataNormalizer:
    _ptp: list
    _min: list
    _segment_length: int
    _features: int

    def __init__(self, data, segment_length, features) -> None:
        self._segment_length = segment_length
        self._features = features
        self._ptp, self._min = self._get_maxes(data)

    def _get_maxes(self, data):
        points = []
        for segment in data:
            for i in range(self._segment_length+1):
                points.append(segment[i*self._features:(i+1)*self._features])
        points = np.array(points)
        return np.tile(points.ptp(0), self._segment_length+1), np.tile(points.min(0), self._segment_length+1)
    
    def normalize(self, data):
        return (data - self._min) / self._ptp

    def unnormalize(self, data):
        return data * self._ptp + self._min


    def unnormalize_output(self, output, value = -1):
        if value == -1:
            return output * self._ptp[1:self._features] + self._min[1:self._features]
        return output[value] * self._ptp[value + 1] + self._min[value + 1]
    
# data = read_data_np(3)
# print(data[0:0 + 2, :])

# normalizer = DataNormalizer(data, 3, 4)
# normed_data = normalizer.normalize(data)
# print(normed_data[:2])
# print(normalizer.unnormalize(normed_data[:2]))

def get_point(point, segment, features):
    point_start = point * features
    point_end = (point + 1) * features
    return segment[point_start:point_end]

def split_data(data, segment_length, features):
    input = []
    labels = []
    # Create sequences of 2 time steps
    for segment in data:
        points = []
        for point in range(segment_length):
            points.append(get_point(point, segment, features))
        input.append(points) # Input sequences of length segment_length with 4 features each
        labels.append(get_point(segment_length, segment, features)[1:]) # ignore time, just lat/long/wind

    # Convert to numpy arrays
    return np.array(input), np.array(labels)

