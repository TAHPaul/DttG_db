import importlib
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

SECTION_LOADERS = {
    'artists': ('scripts.load_artists', 'artists.csv'),
    'artworks': ('scripts.load_artworks', 'artworks.csv'),
    'cities': ('scripts.load_cities', 'cities.csv'),
    'museums': ('scripts.load_museums', 'museums.csv'),
    'colours': ('scripts.load_colours', 'colours.csv'),
    'data': ('scripts.load_data', 'data.csv'),
}

CSV_DIR = Path('data/csv')


class Command(BaseCommand):
    help = (
        'Update the database from CSV loader scripts in data/csv/. '
        'If no section flags are provided, the command prompts for each CSV section.'
    )

    def add_arguments(self, parser):
        parser.add_argument('--all', action='store_true', help='Update every CSV section.')
        parser.add_argument('--artists', action='store_true', help='Update artists.csv.')
        parser.add_argument('--artworks', action='store_true', help='Update artworks.csv.')
        parser.add_argument('--cities', action='store_true', help='Update cities.csv.')
        parser.add_argument('--museums', action='store_true', help='Update museums.csv.')
        parser.add_argument('--colours', action='store_true', help='Update colours.csv.')
        parser.add_argument('--data', action='store_true', help='Update data.csv.')
        parser.add_argument('--dry-run', action='store_true', help='Show what would run without modifying the database.')
        parser.add_argument('--yes', '--no-input', action='store_true', dest='yes', help='Do not prompt; assume all selected sections are confirmed.')

    def handle(self, *args, **options):
        selected_sections = self._determine_sections(options)

        if not selected_sections:
            self.stdout.write(self.style.WARNING('No update sections selected. Nothing to do.'))
            return

        self.stdout.write(self.style.NOTICE('Selected sections: {}').format(', '.join(selected_sections)))

        missing_files = self._validate_csv_files(selected_sections)
        if missing_files:
            raise CommandError(
                'Missing CSV files: ' + ', '.join(str(path) for path in missing_files)
            )

        if options['dry_run']:
            self.stdout.write(self.style.SUCCESS('Dry run complete. No database changes were made.'))
            return

        for section in selected_sections:
            module_name, csv_file = SECTION_LOADERS[section]
            self.stdout.write(self.style.NOTICE(f'Running loader for {section} ({csv_file})...'))
            try:
                module = importlib.import_module(module_name)
                if not hasattr(module, 'run'):
                    raise AttributeError(f"Module '{module_name}' does not define run()")
                module.run()
            except Exception as exc:
                raise CommandError(f"Failed to update '{section}': {exc}")

        self.stdout.write(self.style.SUCCESS('Database update complete.'))

    def _determine_sections(self, options):
        if options['all']:
            return list(SECTION_LOADERS)

        explicit = [name for name in SECTION_LOADERS if options.get(name)]
        if explicit:
            return explicit

        if options['yes']:
            return list(SECTION_LOADERS)

        return [name for name in SECTION_LOADERS if self._prompt_yes_no(name)]

    def _prompt_yes_no(self, section):
        csv_file = SECTION_LOADERS[section][1]
        prompt = f'Update {section} from {csv_file}? [y/N]: '
        if not self.stdin:
            return False
        answer = self.input(prompt).strip().lower()
        return answer in {'y', 'yes'}

    def _validate_csv_files(self, sections):
        missing = []
        for section in sections:
            csv_path = CSV_DIR / SECTION_LOADERS[section][1]
            if not csv_path.exists():
                missing.append(csv_path)
        return missing
