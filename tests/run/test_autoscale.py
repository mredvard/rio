import util


def run_autoscale(stack, *value):

    name = util.rioRun(stack, ' '.join(value), 'nginx')

    return name


def rio_chk_autoscale(stack, sname):
    fullName = (f"{stack}/{sname}")
    inspect = util.rioInspect(fullName)

    return inspect["workingDir"]


def kube_chk_autoscale(stack, service):
    fullName = "%s/%s" % (stack, service)
    id = util.rioInspect(fullName, "id")
    namespace = id.split(":")[0]

    obj = util.kubectl(namespace, "deployment", service)
    cnt = obj['spec']['template']['spec']['containers'][0]
    results = cnt['workingDir']

    return results


def test_autoscale1(stack):
    service_name = run_autoscale(stack, '--scale', '1-10')

    rio_autoscale = rio_chk_autoscale(stack, service_name)
    assert rio_autoscale == "/foo"

    kube_autoscale = kube_chk_autoscale(stack, service_name)
    assert kube_autoscale == "/foo"
