import os
import math
import itertools
from os import path
from configparser import ConfigParser

from .Nsaf import Nsaf
from .LabelSheetSet import LabelSheetSet

class Atlas():
    def __init__(self, dir, lang = None):
        self.lang = lang
        self._base_path = dir
        self._idx_path = path.join(dir, 'idx.na')
        self._dist_path = path.join(dir, 'dist.na')
        self._config_path = path.join(dir, 'config.ini')
        
        assert os.access(self._idx_path, os.R_OK), 'Index image is not readable.'
        assert os.access(self._dist_path, os.R_OK), 'Distance image is not readable.'
        assert os.access(self._config_path, os.R_OK), 'Config file is not readable.'

        self.config = ConfigParser()
        self.config.read(self._config_path)
        
        self.idx_img = Nsaf(self._idx_path)
        self.dist_img = Nsaf(self._dist_path)

        assert self.idx_img.shape == self.dist_img.shape, 'The shape of idx image and dist image is not consistent.'
        assert self.idx_img.offset == self.dist_img.offset, 'The offset of idx image and dist image is not consistent.'

        self.labels = LabelSheetSet(self._base_path)
    
    def query_point(self, coord):
        idx = self.idx_img.query(coord)
        dist = self.dist_img.query(coord)
        label = self.labels.query(idx)

        return {'coord': coord, 'dist': dist, **label}
    
    def _border_min_check(self, x):
        return 0 if x < 0 else x
    
    def _border_max_check(self, x, dim):
        dim_border = self.idx_img.shape[dim] - self.idx_img.offset[dim]
        return dim_border if x > dim_border else x

    def _draw_sphere(self, coord, radius):
        border_min = tuple(map(lambda x: self._border_min_check(coord[x] - radius), range(3)))
        border_max = tuple(map(lambda x: self._border_max_check(coord[x] + radius, x), range(3)))

        mesh = itertools.product(
            range(border_min[0], border_max[0] + 1), 
            range(border_min[1], border_max[1] + 1), 
            range(border_min[2], border_max[2] + 1), 
        )

        target_points = []

        for _p in mesh:
            distance = math.sqrt(sum([(a - b) ** 2 for a, b in zip(_p, coord)]))
            if distance < radius:
                target_points.append(_p)
        
        return target_points
    
    def query_sphere(self, coord, radius):
        coords = self._draw_sphere(coord, radius)

        idxs = list(map(self.idx_img.query, coords))
        dists = list(map(self.dist_img.query, coords))

        count_table = {}

        for _ in range(len(coords)):
            if dists[_] == 0:
                if idxs[_] not in count_table:
                    count_table[idxs[_]] = 1
                else:
                    count_table[idxs[_]] += 1

        result = []

        for _idx in count_table.keys():
            if _idx == 0: 
                continue
            
            label = self.labels.query(_idx)
            label['ratio'] = count_table[_idx] / len(coords)

            result.append(label)

        return sorted(result, key=lambda x: -x['ratio'])

    def query(self, coord, radius = None):
        if radius:
            return self.query_sphere(coord, radius)
        else:
            return self.query_point(coord)

    def batch_query(self, coords, radius = None):
        return list(map(lambda x: self.query(x, radius), coords))