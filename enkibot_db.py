import subprocess
from pathlib import Path
import shutil
import yaml

class Enkibot():
    def __init__(self, jobs:list = None, debug:bool = False) -> None:
        self.hints_path = Path('Enkibot')
        self.hints_repo_url = 'https://github.com/Kyrosiris/Enkibot/'
        if not self.hints_path.is_dir():
            self.refresh_hint_data()

        self.parse_hint_data()

    def refresh_hint_data(self):
        if self.hints_path.is_dir():
            shutil.rmtree(self.hints_path)
        
        self._download_repo()

    def _download_repo(self):
        subprocess.run(['git', 'clone', '--depth', '1', self.hints_repo_url])
    
    def parse_hint_data(self) -> dict:
        data_path = Path(self.hints_path, 'data')
        node_root = Path(data_path, 'nodes.yaml')
        with node_root.open('r') as f:
            nodes_yml = yaml.safe_load(f)

        self.hint_nodes = nodes_yml['Manifest']

        self.raw_hint_data = {'is_complete': False}
        for node in self.hint_nodes:
            node_path = Path(data_path, 'nodes', f'{node}.yaml')
            with node_path.open('r') as f:
                node_yml = yaml.safe_load(f)
                self.raw_hint_data[node] = node_yml

        self.raw_hint_data['is_complete'] = True

        return self.raw_hint_data



if __name__ == '__main__':
    bot = Enkibot()
    print(bot.hints_path)
    print(bot.hints_repo_url)
    print(bot.hint_nodes)
    print(bot.raw_hint_data['versions'])

# command = 'git clone --depth 1 --no-checkout'
