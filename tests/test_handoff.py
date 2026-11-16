import os, subprocess, sys, tempfile, pathlib
H = str(pathlib.Path(__file__).resolve().parent.parent / 'scripts' / 'handoff.py')
def sh(cwd, *a, env=None):
    return subprocess.run(a, cwd=cwd, capture_output=True, text=True, env={**os.environ, **(env or {})})
def hand(cwd, *a, agent='a1'):
    return sh(cwd, sys.executable, '-B', H, '--offline', '--agent', agent, *a)
with tempfile.TemporaryDirectory() as t:
    sh(t, 'git', 'init', '-q', '-b', 'main'); sh(t, 'git', 'config', 'user.email', 'x@x'); sh(t, 'git', 'config', 'user.name', 'x')
    open(f'{t}/a.txt', 'w').write('1'); sh(t, 'git', 'add', '.'); sh(t, 'git', 'commit', '-qm', 'init')
    head = sh(t, 'git', 'rev-parse', 'HEAD').stdout
    # uncommitted + untracked + secret
    open(f'{t}/a.txt', 'w').write('2'); open(f'{t}/new.txt', 'w').write('n'); open(f'{t}/.env', 'w').write('SECRET=1')
    r = hand(t, 'save', '--note', 'wip'); assert r.returncode == 0, r.stderr
    refs = sh(t, 'git', 'for-each-ref', 'refs/handoff').stdout; assert 'refs/handoff/a1/main' in refs, refs
    files = sh(t, 'git', 'ls-tree', '-r', '--name-only', 'refs/handoff/a1/main').stdout.split()
    assert 'new.txt' in files and '.env' not in files, files          # untracked kept, secret excluded
    assert sh(t, 'git', 'rev-parse', 'HEAD').stdout == head            # branch untouched
    assert open(f'{t}/a.txt').read() == '2' and sh(t, 'git', 'status', '--porcelain').stdout.count('\n') >= 2
    # claims: second agent refused, release frees
    assert hand(t, 'claim', 'T1', agent='a1').returncode == 0
    assert hand(t, 'claim', 'T1', agent='a2').returncode != 0
    assert hand(t, 'release', 'T1', agent='a1').returncode == 0
    assert hand(t, 'claim', 'T1', agent='a2').returncode == 0
    # resume --apply restores work on a new branch
    assert hand(t, 'resume', '--apply', 'a1/main', agent='a2').returncode != 0   # refuses on a dirty tree
    sh(t, 'git', 'stash', '-u', '-q')
    r = hand(t, 'resume', '--apply', 'a1/main', agent='a2'); assert r.returncode == 0, r.stderr + r.stdout
    assert open(f'{t}/a.txt').read() == '2' and open(f'{t}/new.txt').read() == 'n' and not os.path.exists(f'{t}/.env')
print('ok')
