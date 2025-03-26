{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
		packages = with pkgs; [
			(python312.withPackages(p: with p; [
				python-lsp-server
			]))
		];
		shellHook = ''
			if [ ! -d "./.pyvenv" ]
			then
				python -m venv ./.pyvenv
				./.pyvenv/bin/pip install -r requirements.txt
			fi

			source ./.pyvenv/bin/activate
		'';
	}
