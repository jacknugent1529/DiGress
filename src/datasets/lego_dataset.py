import os
import torch
from torch.utils.data import Dataset, random_split
from src.datasets.abstract_dataset import AbstractDataModule, AbstractDatasetInfos

class LegoGeoDataset(Dataset): # this should be self-contained
    def __init__(self):
        base_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, os.pardir, 'data')
        filename = os.path.join(base_path, 'lego_geo_data.pt')
        self.data = torch.load(filename)
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, i):
        return self.data[i]

class GeneralLegoGeoDataModule(AbstractDataModule):
    def __init__(self, cfg):
        super().__init__(cfg)
        self.prepare_data()
        self.inner = self.train_dataloader()

    def __getitem__(self, item):
        return self.inner[item]

    def prepare_data(self, graphs):
        test_len = int(round(len(graphs) * 0.2))
        train_len = int(round((len(graphs) - test_len) * 0.8))
        val_len = len(graphs) - train_len - test_len
        print(f'Dataset sizes: train {train_len}, val {val_len}, test {test_len}')
        splits = random_split(graphs, [train_len, val_len, test_len], generator=torch.Generator().manual_seed(1234))

        datasets = {'train': splits[0], 'val': splits[1], 'test': splits[2]}
        super().prepare_data(datasets)

class LegoGeoDataModule(GeneralLegoGeoDataModule):
    def prepare_data(self):
        graphs = LegoGeoDataset()
        return super().prepare_data(graphs)


class LegoGeoDatasetInfos(AbstractDatasetInfos):
    def __init__(self, datamodule, dataset_config):
        self.datamodule = datamodule
        self.name = 'lego_graphs'
        self.n_nodes = self.datamodule.node_counts()
        self.node_types = torch.tensor([0,1,2])               # There are no node types
        self.edge_types = self.datamodule.edge_counts()
        super().complete_infos(self.n_nodes, self.node_types)

