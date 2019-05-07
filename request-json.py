import json
import requests
import numpy as np
from matplotlib import pyplot as plt
api = ''

# returns a lerp of azimuth and elevation in the interval [t+1, t+11]
def getnext10seconds(lat, lng, alt):
    url = 'https://www.n2yo.com/rest/v1/satellite/positions/25544/{}/{}/{}/10/&apiKey={}'.format(lat,lng,alt,'SBRY9Q-LVVSFA-L6KE5G-3ZSV')


    resp = requests.get(url)
    data = resp.json()
    azimuths = [data['positions'][t]['azimuth'] for t in range(10)]
    elevations = [data['positions'][t]['elevation'] for t in range(10)]
    azimuth = lambda a: np.interp(a, range(10), azimuths)
    elevation = lambda a: np.interp(a, range(10), elevations)
    return (azimuth, elevation)

x = np.linspace(0, 10, 50)
data = getnext10seconds(0,0,0)
fig = plt.figure()
ax1 = fig.add_subplot(211, projection='polar')
ax2 = fig.add_subplot(212, projection='polar')
# plt.ylim((0,90))
plt.subplot(2,1,1)
plt.title('Uphead')
plt.ylim(-90.0,0)
plt.plot(data[0](x), -data[1](x))
plt.subplot(2,1,2)
plt.title('Downhead')
plt.ylim(-90.0,0)
plt.plot(data[0](x), data[1](x))

plt.show()

# >>> x = np.linspace(0, 2*np.pi, 10)
# >>> y = np.sin(x)
# >>> xvals = np.linspace(0, 2*np.pi, 50)
# >>> yinterp = np.interp(xvals, x, y)
# >>> import matplotlib.pyplot as plt
# >>> plt.plot(x, y, 'o')
# [<matplotlib.lines.Line2D object at 0x...>]
# >>> plt.plot(xvals, yinterp, '-x')
# [<matplotlib.lines.Line2D object at 0x...>]
# >>> plt.show()
